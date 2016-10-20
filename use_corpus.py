import gensim
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_cleaned")
corpus = gensim.corpora.MmCorpus('corpus.mm.gz')

# This creates a tf_idf transformation function that can be applied to any
# document vector (from the same dictionary)
#tfidf = gensim.models.TfidfModel(corpus)
tfidf = gensim.models.TfidfModel.load("tfidf_model")

#print "Finished calculating tfidf"
#tfidf.save("tfidf_model")

# Creates a transformed object instance. Note that this will not proccess
# anything yet
#corpus_tfidf = tfidf[corpus]
corpus_tfidf = gensim.corpora.MmCorpus('corpus_tfidf.mm')
#gensim.corpora.MmCorpus.serialize("corpus_tfidf.mm", corpus_tfidf)

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
lsi.save("lsi_model")
corpus_lsi = lsi[corpus_tfidf]
gensim.corpora.MmCorpus.serialize("corpus_lsi.mm", corpus_lsi)
