import math
import redis
import Queue
import re
from nltk.stem.porter import PorterStemmer
from collections import Counter


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


class TFIDFDocLen(TFIDF):
    def __init__(self):
        super(TFIDFDocLen, self).__init__()

    def __avg_doclen(self):
        return int(self._r.get('avg_doclen'))

    def __get_doclen(self, did):
        return int(self._r.get('doclen::' + did))

    def tf(self, term, tf_did, b=0.2):
        final_term_count = 0

        for did_entry in self._r.lrange(self.redis_path(term), 0, -1):
            did_entry_split = did_entry.split('|')

            did = did_entry_split[0]
            term_count = int(did_entry_split[1])

            if tf_did == did:
                final_term_count = term_count

        return float(final_term_count) / \
            (1 - b + (b * (self.__get_doclen(tf_did) / self.__avg_doclen())))


class TIQuery(object):
    def __init__(self):
        self._t = TFIDFDocLen()
        self._r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self._stemmer = PorterStemmer()
        self._num_split_re = re.compile('[A-Za-z_]+')

    def query(self, query_vector, num_query=10):
        doc_set = set()
        base_word_vector = [self._stemmer.stem(word) for word in query_vector]

        for w in base_word_vector:
            for did in self._t.term_docs(w):
                doc_set.add(did)

        top_dids = Queue.PriorityQueue()

        for did in doc_set:
            ti_sum = 0.0
            for w in base_word_vector:
                if self._r.exists(self._t.redis_path(w)):
                    ti_sum = ti_sum + self._t.tf_idf(w, did)

            if ti_sum != 0.0:
                top_dids.put((-1 * ti_sum, did))

        prio_dids = []
        for i in xrange(num_query):
            if top_dids.empty() is False:
                prio_dids.append(top_dids.get_nowait())

        return [did_t[1] for did_t in prio_dids]

    def histQuery(self, query_vector):
        query_results = self.query(query_vector)

        stripped_query_results = [re.search(self._num_split_re, did).group(0) for did in query_results]

        did_counter = Counter(stripped_query_results)
        return [item for item, count in did_counter.most_common()]


def tfidf_test(word):
    t = TFIDF()
    print 'Word: ' + word
    print t.term_docs(word)
    for did in t.term_docs(word):
        print 'Document: ' + str(did)
        print 'TF: ' + str(t.tf(word, did))
        print 'IDF: ' + str(t.idf(word))
        print 'TF-IDF: ' + str(t.tf_idf(word, did))
        print ''

    q = TIQuery()
    for did in q.histQuery('coughing and fever'.split()):
        print 'Document found: ' + did


if __name__ == "__main__":
    tfidf_test('loss')
