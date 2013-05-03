import math
import redis

class TFIDF(object):
	def __init__(self):
		self._r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def __total_num_docs(self):
		return int(self._r.get('total_doc_num'))

	def redis_path(self, term):
		return 'term::'+term

	def tf(self, term):
		total_term_count = 0

		for did_entry in self._r.lrange(self.redis_path(term), 0, -1):
			did_entry_split = did_entry.split('|')
			did = did_entry_split[0]
			term_count = int(did_entry_split[1])
			total_term_count = total_term_count + term_count

		return total_term_count

	def idf(self, term):
		return math.log( float(self.__total_num_docs()) / float(self._r.llen(self.redis_path(term))) )


	def tf_idf(self, term):
		return self.tf(term) * self.idf(term)

if __name__ == "__main__":
	t = TFIDF()
	print 'TF: ' + str(t.tf('term1'))
	print 'IDF: ' + str(t.idf('term1'))
	print 'TF-IDF: ' + str(t.tf_idf('term1'))
