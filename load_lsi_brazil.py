import psycopg2
import gensim
import logging
import json

with open("corpus2db_brazil", "r") as f:
    corpus2db = json.load(f)
    corpus2db = {int(key): val for (key, val) in corpus2db.iteritems()}

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_brazil")
corpus = gensim.corpora.MmCorpus('corpus_lsi_brazil.mm')

tfidf = gensim.models.TfidfModel.load("tfidf_model_brazil")

lsi = gensim.models.LsiModel.load("lsi_model_brazil")
lsi.print_topics()

index = gensim.similarities.MatrixSimilarity(corpus, num_features=100)
index.save("corpus_brazil.index")


def transform(query):
    vec_query = dictionary.doc2bow(query.lower().split())
    query_tfidf = tfidf[vec_query]
    return lsi[query_tfidf]

con = psycopg2.connect("dbname='base' user='alice'")
print "Conectado a db"
cur = con.cursor()

while True:
    query = raw_input("Please type your query: ")
    if query == "q":
        con.close()
    query_lsi = transform(query)
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:10]
    cur.execute("SELECT * FROM cable WHERE id = %i;" % corpus2db[sims[0][0]])
    print cur.fetchall()[0][-1]
