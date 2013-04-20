from tornado.web import RequestHandler
from handlers.gsearch import GoogleSearchRequest
import json


class QueryHandler(RequestHandler):

    def post(self):
    	self.set_header("Content-Type", "application/json")
    	postDict = json.loads(self.request.body)
    	g = GoogleSearchRequest()
    	q = g.search('pickle')
    	print 'here: \n'  + q
    	self.write(json.dumps(q))
    	self.finish()
