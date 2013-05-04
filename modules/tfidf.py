import math
import redis
import Queue


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

        return 0    # Return 0 by default if the term is not found

    def term_docs(self, term):
        dids = self._r.lrange(self.redis_path(term), 0, -1)
        return [did_pack.split('|')[0] for did_pack in dids]

    def idf(self, term):
        return math.log(float(self.__total_num_docs()) / float(self._r.llen(self.redis_path(term))))

    def tf_idf(self, term, did):
        return self.tf(term, did) * self.idf(term)


class TIQuery(object):
    def __init__(self):
        self._t = TFIDF()
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def query(self, query_vector, num_query=10):
        doc_set = set()

        for w in query_vector:
            for did in self._t.term_docs(w):
                doc_set.add(did)

        top_dids = Queue.PriorityQueue()

        for did in doc_set:
            ti_sum = 0.0
            for w in query_vector:
                if self._r.exists(self._t.redis_path(w)):
                    ti_sum = ti_sum + self._t.tf_idf(w, did)

            if ti_sum != 0.0:
                top_dids.put((-1 * ti_sum, did))

        prio_dids = []
        for i in xrange(num_query):
            if top_dids.empty() is False:
                prio_dids.append(top_dids.get_nowait())

        return [did_t[1] for did_t in prio_dids]


def tfidf_test(word):
    t = TFIDF()
    print 'Word: ' + word
    for did in t.term_docs(word):
        print 'Document: ' + str(did)
        print 'TF: ' + str(t.tf(word, did))
        print 'IDF: ' + str(t.idf(word))
        print 'TF-IDF: ' + str(t.tf_idf(word, did))
        print ''

    q = TIQuery()
    for did in q.query('appetite loss chills'.split()):
        print 'Document found: ' + did


if __name__ == "__main__":
    tfidf_test('appetite')
