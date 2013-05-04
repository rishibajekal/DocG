import redis
import os
import json


class InvertedIndexBuilder(object):
    def __has_json_ext(self, string):
        return string.find('.json') != -1

    def __process_json(self, json_path):
        with open(json_path, 'r') as json_file:
            json_obj = json.load(json_file)
            print json_obj['documents']
            for did, term_dict in json_obj['documents'].items():
                for term, term_occur in term_dict.items():
                    print "Document ID: " + did + " Term: " + term
                    self._r.lpush('term::'+term, did+'|'+str(term_occur))
            return len(json_obj['documents'].keys())

    def __add_docnum(self, doc_num):
        self._r.set('total_doc_num', doc_num)

    def __init__(self, folder_dir=None):
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0)

        if folder_dir is None:
            folder_path = os.path.join(os.path.dirname(__file__), "../illness_docs")
        else:
            folder_path = os.path.join(os.path.dirname(__file__), "../" + folder_dir)

        folder_contents = os.listdir(folder_path)
        total_docs = 0

        for file_name in folder_contents:
            if self.__has_json_ext(file_name):
                full_file_name = os.path.join(folder_path, file_name)
                print full_file_name
                docs_in_json = self.__process_json(full_file_name)
                total_docs = total_docs + docs_in_json

        self.__add_docnum(total_docs)
