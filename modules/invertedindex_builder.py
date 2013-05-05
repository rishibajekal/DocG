import redis
import os
import json
from collections import defaultdict


class InvertedIndexBuilder(object):
    def __has_json_ext(self, string):
        return string.find('.json') != -1

    def __process_json(self, json_path):
        print "Processing JSON in ", json_path
        with open(json_path, 'r') as json_file:
            json_obj = json.load(json_file)
            num_docs = 0
            for did, term_dict in json_obj['documents'].items():
                num_docs = num_docs + 1
                doc_len = 0
                for term, term_occur in term_dict.items():
                    self._r.lpush('term::'+term, did+'|'+str(term_occur))
                    doc_len = doc_len + 1
                self._doc_len_dict[did] = doc_len
            return len(json_obj['documents'].keys())
            #return num_docs

    def __add_docnum(self, doc_num):
        self._r.set('total_doc_num', doc_num)

    def __avg_doclen(self):
        v = self._doc_len_dict.values()
        return sum(v) / len(v)

    def __store_doclen(self):
        for did, doc_len in self._doc_len_dict.items():
            self._r.set('doclen::'+did, doc_len)

    def __store_avg_doclen(self):
        self._r.set('avg_doclen', self.__avg_doclen())

    def __init__(self, folder_dir=None):
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._doc_len_dict = defaultdict(int)

        if folder_dir is None:
            folder_path = os.path.join(os.path.dirname(__file__), "../illness_docs")
        else:
            folder_path = os.path.join(os.path.dirname(__file__), "../" + folder_dir)

        folder_contents = os.listdir(folder_path)
        total_docs = 0

        for file_name in folder_contents:
            if self.__has_json_ext(file_name):
                full_file_name = os.path.join(folder_path, file_name)
                docs_in_json = self.__process_json(full_file_name)
                total_docs = total_docs + docs_in_json

        self.__add_docnum(total_docs)
        self.__store_doclen()
        self.__store_avg_doclen()
