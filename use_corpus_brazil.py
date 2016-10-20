import gensim
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_brazil")
corpus = gensim.corpora.MmCorpus('corpus_brazil.mm')

# This creates a tf_idf transformation function that can be applied to any
# document vector (from the same dictionary)
#tfidf = gensim.models.TfidfModel(corpus)
#print "Finished calculating tfidf"
#tfidf.save("tfidf_model_brazil")


tfidf = gensim.models.TfidfModel.load("tfidf_model_brazil")
# Creates a transformed object instance. Note that this will not proccess
# anything yet
#corpus_tfidf = tfidf[corpus]
#gensim.corpora.MmCorpus.serialize("corpus_tfidf_brazil.mm", corpus_tfidf)

corpus_tfidf = gensim.corpora.MmCorpus('corpus_tfidf_brazil.mm')
lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)
lsi.save("lsi_model_brazil")
corpus_lsi = lsi[corpus_tfidf]
gensim.corpora.MmCorpus.serialize("corpus_lsi_brazil.mm", corpus_lsi)
