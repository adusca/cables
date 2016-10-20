import psycopg2
import gensim
import logging
import os

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_cleaned")
lda = gensim.models.wrappers.ldamallet.LdaMallet.load("lda_model_100")
lda.mallet_path = os.path.expanduser('~/FGV/cablegate/mallet/bin/mallet')
corpus = gensim.corpora.MmCorpus('corpus_lda_100.mm')

lda.print_topics(50)
#for x in corpus[:20]:
#    print [(dictionary[bow_id], prob) for (bow_id, prob) in x]

index = gensim.similarities.MatrixSimilarity(corpus, num_features=100)


def transform(query):
    vec_query = dictionary.doc2bow(query.lower().split())
    print vec_query
    return lda[vec_query]

con = psycopg2.connect("dbname='base' user='alice'")
print "Conectado a db"
cur = con.cursor()

while True:
    query = raw_input("Please type your query: ")
    query_lda = transform(query)
    print query_lda
    sims = index[query_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:10]
    print sims
    cur.execute("SELECT * FROM cable WHERE id = %i;" % (sims[0][0]+1))
    print sims[0][0]
    print cur.fetchall()
