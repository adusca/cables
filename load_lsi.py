import psycopg2
import gensim
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_cleaned")
corpus = gensim.corpora.MmCorpus('corpus_lsi.mm')

tfidf = gensim.models.TfidfModel.load("tfidf_model")

lsi = gensim.models.LsiModel.load("lsi_model")
#lsi.print_topics(10)

#index = gensim.similarities.MatrixSimilarity(corpus, num_features=100)
#index.save("corpus100.index")
index = gensim.similarities.MatrixSimilarity.load("corpus100.index")


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
    print sorted(query_lsi, key=lambda item: -item[1])
    print lsi.print_topic(43)
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:10]
    print sims
    cur.execute("SELECT * FROM cable WHERE id = %i;" % (sims[0][0] + 1))
    print sims[0][0]
    print cur.fetchall()
