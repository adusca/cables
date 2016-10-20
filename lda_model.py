import gensim
import logging
import os

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)


d = gensim.corpora.Dictionary()

dictionary = d.load("binary_dict_cleaned")
corpus = gensim.corpora.MmCorpus('corpus.mm.gz')

n = 100
lda = gensim.models.wrappers.ldamallet.LdaMallet(
    os.path.expanduser('~/FGV/cablegate/mallet/bin/mallet'),
    corpus=corpus, num_topics=n, id2word=dictionary, optimize_interval=10,
    workers=8)
lda.save("lda_model_%i" % n)
corpus_lda = lda[corpus]
gensim.corpora.MmCorpus.serialize("corpus_lda_%i.mm" % n, corpus_lda)
