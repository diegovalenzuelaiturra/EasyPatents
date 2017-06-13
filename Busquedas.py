from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
#from nltk.stem import SnowballStemmer
#from nltk.stem import WordNetLemmatizer
from nltk.collocations import *
from nltk import pos_tag
import nltk
from translate import Translator


def translateText(lengin,lengout,text):
    return Translator(from_lang=lengin, to_lang=lengout).translate(text)


def translateWord(lengin,lengout,text):
    aux = []
    for i in text:
        aux.append(Translator(from_lang=lengin, to_lang=lengout).translate(i))
    return aux


def deletePunt(text):
    return RegexpTokenizer(r'\w+').tokenize(text)


def deleteStop(leng, text):
    stop = set(stopwords.words(leng))
    aux = text
    for i in aux:
        if i in stop:
            aux.remove(i)
    return aux


def stemmingPorter(text):
    ps = PorterStemmer()
    sent = pos_tag(text)
    aux = list()
    for i in sent:
        if i[1]=='NN':
            aux.append(i[0])
        else:
            aux2 = ps.stem(i[0])
            if aux2 != i[0]:
                aux.append(aux2 + '*')
            else:
                aux.append(aux2)
    return aux


def stemmingSnowball(leng,text):
    ps = SnowballStemmer(leng)
    aux1 = text
    for i in range(len(text)):
        aux2 = ps.stem(aux1[i])
        if aux2 != aux1[i]:
            aux1[i] = aux2 + '*'
        else:
            aux1[i] = aux2
    return aux1


def stemmingLemmatizer(text):
    ps = WordNetLemmatizer()
    aux1 = text
    for i in range(len(text)):
        aux1[i] = ps.lemmatize(aux1[i])
    return aux1


def collocationFinder(nmin,nmax,words):
    rango = range(nmin,nmax)
    lista = list()
    for i in rango:
        n_vent = i
        finder1 = BigramCollocationFinder.from_words(words, window_size=n_vent)
        finder1.apply_freq_filter(2)
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        aux = finder1.score_ngrams(bigram_measures.pmi)
        for j in aux:
            if abs(j[1]) > 0.5: #valor minimo correlacion
                lista.append(j[0][0] + ' $w' + str(n_vent) + ' ' + j[0][1])

    return lista

def deleteWord(type,words):
    aux = list()
    sent = pos_tag(words)
    for i in sent:
        if i[1]==type:
            pass
        else:
            aux.append(i[0])
    return aux