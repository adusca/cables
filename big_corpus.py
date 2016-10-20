import psycopg2
import string
import logging
import json
from gensim import corpora

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary().load("binary_dict_cleaned")

query = "SELECT * FROM cable"

class CablesCorpus:
    def __iter__(self):
        # Conectando ao banco de dados
        con = psycopg2.connect("dbname='base' user='alice'")
        print "Conectado a db"
        cur = con.cursor()
        cur.execute(query)
        while True:
            row = cur.fetchone()
            if row is None:
                break
            to_remove = string.punctuation + string.digits
            table = string.maketrans(to_remove, " "*len(to_remove))
            document = row[-1].translate(table).lower()
            yield dictionary.doc2bow(document.split(), allow_update=False)

corpus = CablesCorpus()

corpora.MmCorpus.serialize('corpus.mm', corpus)
# i = 0
# for x in corpus:
#     i+= 1
#     if i % 10000 == 0:
#         print i

# print dictionary
# print corpus
# dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None)
# print dictionary
# dictionary.save("binary_dict_cleaned")
# dictionary.save_as_text("dictionary.txt", sort_by_word=False)
