from tornado.web import RequestHandler
import json


class QueryHandler(RequestHandler):

    def post(self):
        self.set_header("Content-Type", "application/json")
        postDict = json.loads(self.request.body)
        self.write(json.dumps({"success": True, "data": json.dumps(postDict)}))
