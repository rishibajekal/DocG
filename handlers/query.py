from tornado.web import RequestHandler
from modules.tfidf import TIQuery
import json
import re


class QueryHandler(RequestHandler):

    def post(self):
        self.set_header("Content-Type", "application/json")
        postDict = json.loads(self.request.body)
        user_input = postDict["query"]

        ranker = TIQuery()
        rel_doc_ids = ranker.query(user_input.split())

        illnesses = self.__get_illness_names(rel_doc_ids)

        if len(rel_doc_ids) != 0:
            self.write(json.dumps({"success": True, "data": illnesses}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()

    def __get_illness_names(self, doc_ids):
        illnesses = []

        for did in doc_ids:
            formatted_name = did.replace("_", " ")
            illness_name = re.sub(r"\d", "", formatted_name)
            illnesses.append(illness_name)

        return illnesses
