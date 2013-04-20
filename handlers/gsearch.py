import requests
import json


class SearchException(Exception):
	def __init__(self, message):
		self.message = message


class GoogleSearchRequest(object):

	cx = '007752576480906932928:s9ewnuvanf4'
	api_key = 'AIzaSyDE6IKKJJuCbKs0k_TaSbIIEew0-h8VNmM'
	base_url = 'https://www.googleapis.com/customsearch/v1'

	def __init__(self):
		pass

	def search(self, query, numResults=10):
		params_dict = {'cx': self.cx, 'key': self.api_key, 'q': query, 'alt': 'json', 'startIndex':0, 'num':10}

		print params_dict

		outResults = []

		totalPages = (numResults / 10) + 1

		for currPage in xrange(totalPages):
			params_dict['startIndex'] = currPage * 10 + 1
			if currPage == totalPages - 1:
				params_dict['num'] = numResults % 10

			results = json.loads(requests.get(self.base_url, params=params_dict).text)

			if 'items' not in results:
				print results
				raise SearchException('No results found')
			else:
				for result in results['items']:
					resultDict = {}
					resultDict['title'] = result['title']
					resultDict['link'] = result['link']
					resultDict['displayLink'] = result['displayLink']
					resultDict['snippet'] = result['snippet']
					outResults.append(resultDict)

			
		return outResults



if __name__ == "__main__":
	g = GoogleSearchRequest()
	searchResults = g.search("obama", 21)

	print "Found " + str(len(searchResults)) + " results"
	print searchResults
