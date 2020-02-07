import numpy as np
import math
import scipy
import gensim, logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)
model = gensim.models.KeyedVectors.load_word2vec_format(
    './GoogleNews-vectors-negative300.bin.gz', binary=True)

model.most_similar(positive=[model['hot']], topn=1)
