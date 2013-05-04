from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
import urllib2
import re
import os


class SymptomScraper(object):

    path = os.path.join(os.path.dirname(__file__), '../resources/medical_terms.txt')

    def __init__(self, path=None):
        self.stemmer = PorterStemmer()
        if path is None:
            self.sym_set = self.__get_symptom_set(self.path)
        else:
            self.sym_set = self.__get_symptom_set(path)

    def get_symptoms(self, url, path=None):
        return self.__scrape(url)

    def __get_symptom_set(self, path):
        f = open(path)
        sym_set = set()
        for symptom in f:
            base_sym_word = self.stemmer.stem(symptom.strip().lower())
            sym_set.add(base_sym_word)
        return sym_set

    def __is_symptom(self, word):
        return word in self.sym_set

    def __scrape(self, url):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = urllib2.Request(url, headers=hdr)
        html = urllib2.urlopen(request)
        soup = BeautifulSoup(html)

        symptoms = []
        for line in soup.findAll(text=True):
            for word in re.findall(r"\w+", line):
                base_word = self.stemmer.stem(word.lower())
                if self.__is_symptom(base_word):
                    symptoms.append(base_word)
        return symptoms
