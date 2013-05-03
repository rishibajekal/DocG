from bs4 import BeautifulSoup
import urllib2
import re
import os


class SymptomScraper(object):

    path = os.path.join(os.path.dirname(__file__), '../resources/medical_terms.txt')

    def __init__(self, path=None):
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
            sym_set.add(symptom.strip().lower())
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
                if self.__is_symptom(word):
                    symptoms.append(word)
        return symptoms
