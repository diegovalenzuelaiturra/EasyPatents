from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.corpus import wordnet
from nltk.collocations import *
from nltk import pos_tag
import nltk
from translate import Translator
from BusquedasEPO import *

def translateText(lengin,lengout, text):
    return Translator(from_lang=lengin, to_lang=lengout).translate(text)


def translateTextAuto(lengout, text):
    return Translator(from_lang='auto', to_lang=lengout).translate(text)


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
    aux1 = text
    for i in range(len(text)):
        aux2 = ps.stem(aux1[i])
        if aux2 != aux1[i]:
            aux1[i] = aux2 + '*'
        else:
            aux1[i] = aux2
    return aux1


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
        aux2 = ps.lemmatize(aux1[i])
        if aux2 != aux1[i]:
            aux1[i] = aux2 + '*'
        else:
            aux1[i] = aux2
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


def getType(type,word):
    sent = pos_tag(word)
    if sent[1]==type:
        return True
    else:
        return False


def minimizar(text):
    return  text.lower()


def get_synonymous(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms


def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return antonyms


def similaridad(word1,word2):
    w1 = wordnet.synsets(word1)[0]
    w2 = wordnet.synsets(word2)[0]
    return w1.wup_similarity(w2)


def preProcessing(text):
    sentences = text.split(';')
    senEn = []
    for sentence in sentences:
        aux = translateText(lengin='es',lengout='en', text=sentence)
        aux = deletePunt(text=aux)
        #aux = deleteStop(text=aux, leng='english')
        aux = stemmingLemmatizer(aux)
        senEn.append(aux)
    cql = countryEPO()+' and '
    for i in range(len(senEn)):
        if i == 0:
            cql += allEPO('ta',senEn[i])
        else:
            cql = orEPO(cql,allEPO('ta',senEn[i]))
    return cql