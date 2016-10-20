import psycopg2
import string
import logging
import json
from gensim import corpora

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dict_brazil = corpora.Dictionary().load("binary_dict_brazil")
corpus2db = {}
#dictionary = corpora.Dictionary().load("binary_dict")
#dictionary.filter_extremes(no_below=1, no_above=0.5, keep_n=None)

query = "SELECT * FROM cable"
query_brazil = """SELECT * FROM cable
                 WHERE (origin='Embassy Brasilia'
                        OR origin='Consulate Sao Paulo'
                        OR origin='Consulate Rio De Janeiro'
                        OR origin='Consulate Recife');"""


class CablesCorpus:
    def __init__(self):
        self.doc_count = 0

    def __iter__(self):
        # Conectando ao banco de dados
        con = psycopg2.connect("dbname='base' user='alice'")
        print "Conectado a db"
        cur = con.cursor()
        cur.execute(query_brazil)
        print "Selecionando todas as linhas originadas no Brazil"
        while True:
            row = cur.fetchone()
            if row is None:
                break
            corpus2db[self.doc_count] = row[0]
            self.doc_count += 1
            to_remove = string.punctuation + string.digits
            table = string.maketrans(to_remove, " "*len(to_remove))
            text = row[-1].split("SUBJECT:")[-1]
            document = text.translate(table).lower()
            yield dict_brazil.doc2bow(document.split(), allow_update=False)

corpus = CablesCorpus()

corpora.MmCorpus.serialize('corpus_brazil.mm', corpus)

print dict_brazil
print corpus
with open("corpus2db_brazil", 'w') as f:
    json.dump(corpus2db, f)
# dict_brazil.filter_extremes(no_below=5, no_above=0.5, keep_n=None)
# print dict_brazil
# dict_brazil.save("binary_dict_brazil")
# dict_brazil.save_as_text("dict_brazil.txt", sort_by_word=False)
