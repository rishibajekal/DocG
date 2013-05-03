from scraper import SymptomScraper
from collections import defaultdict
import os
import json


class DocumentBuilder(object):

    path = os.path.join(os.path.dirname(__file__), "../resources/illness_urls.json")
    directory = os.path.join(os.path.dirname(__file__), "../illness_docs/")

    def __init__(self, path=None):
        if path is None:
            f = open(self.path)
        else:
            f = open(path)
        self.illness_json = json.load(f)
        self.scraper = SymptomScraper()

    def build_documents(self):
        for illness in self.illness_json["illnesses"]:
            name = illness["illness"]
            illness_docs = {}
            url_counter = 0

            for url in illness["urls"]:
                document_dict = defaultdict(int)
                symp_list = self.scraper.get_symptoms(url)
                for symptom in symp_list:
                    document_dict[symptom] += 1
                doc_id = name + str(url_counter)
                illness_docs[doc_id] = document_dict
                url_counter += 1

            illness_dict = dict()
            illness_dict["documents"] = illness_docs

            self.__write_json_file(name, illness_dict)

    def __write_json_file(self, illness_name, illness_dict):
        f = open(self.directory + illness_name + ".json", "w")
        json.dump(illness_dict, f)


sb = DocumentBuilder()
sb.build_documents()
