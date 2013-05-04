from tornado.web import RequestHandler
from modules.tfidf import TIQuery
import json


class QueryHandler(RequestHandler):

    def post(self):
        self.set_header("Content-Type", "application/json")
        postDict = json.loads(self.request.body)
        user_input = postDict["query"]

        ranker = TIQuery()
        rel_doc_ids = ranker.query(user_input.split())

        if len(rel_doc_ids) != 0:
            self.write(json.dumps({"success": True, "data": rel_doc_ids}))
        else:
            self.write(json.dumps({"success": False}))
        self.finish()
