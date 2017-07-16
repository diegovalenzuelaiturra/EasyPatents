from gensim.models.wrappers import FastText
import gensim, logging


def gloveTovec(glove_input,word2vec_output):
    gensim.scripts.glove2word2vec.glove2word2vec(glove_input, word2vec_output)

def loadFastText(fasttex_input):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = FastText.load_fasttext_format(fasttex_input)
    return model

def loadModel(input,binary):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#model = gensim.models.KeyedVectors.load_word2vec_format('../GoogleNews-vectors-negative300.bin.gz', binary=True)
    model = gensim.models.KeyedVectors.load_word2vec_format(input, binary=binary)
    return model

glove = '~/Documentos/glove.6B/glove.6B.300d.txt'
vec = '~/Documentos/glove.6B/wiki.txt'
gloveTovec(glove,vec)