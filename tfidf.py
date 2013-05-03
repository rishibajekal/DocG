import math
import redis

class TFIDF(object):
	def __init__(self):
		self._r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def __total_num_docs(self):
		return int(self._r.get('total_doc_num'))

	def redis_path(self, term):
		return 'term::'+term

	def tf(self, term, tf_did):
		for did_entry in self._r.lrange(self.redis_path(term), 0, -1):
			did_entry_split = did_entry.split('|')

			did = did_entry_split[0]
			term_count = int(did_entry_split[1])

			if tf_did == did:
				return term_count

		return 0 # Return 0 by default if the term is not found

	def term_docs(self, term):
		dids = self._r.lrange(self.redis_path(term), 0, -1)
		return [did_pack.split('|')[0] for did_pack in dids]

	def idf(self, term):
		return math.log( float(self.__total_num_docs()) / float(self._r.llen(self.redis_path(term))) )


	def tf_idf(self, term, did):
		return self.tf(term, did) * self.idf(term)

def tfidf_test(word):
	t = TFIDF()
	print 'Word: ' + word
	for did in t.term_docs(word):
		print 'Document: ' + str(did)
		print 'TF: ' + str(t.tf(word, did))
		print 'IDF: ' + str(t.idf(word))
		print 'TF-IDF: ' + str(t.tf_idf(word, did))
		print ''


if __name__ == "__main__":
	tfidf_test('appetite')
