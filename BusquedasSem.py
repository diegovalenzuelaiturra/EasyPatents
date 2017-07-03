from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import *
from nltk.corpus import wordnet
from nltk.collocations import *
from nltk import pos_tag
import nltk
from translate import Translator
from BusquedasEPO import *
import csv
import pandas as pd
#from googletrans import Translator
import numpy as np
import math
import scipy
import gensim, logging


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin.gz', binary=True)


def gosTranslateText(langin,langout, text):
    #try:
        translator = Translator()
        aux = translator.translate(text, dest=langout)#, src=langin)
        return aux.text
    #except:
    #    print("Error en la traducción")

def translateText(lengin,lengout, text):
    try:
        return Translator(from_lang=lengin, to_lang=lengout).translate(text)
    except:
        print("Error en la traducción")

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
        #    aux1[i] = aux2 + '*'
            aux1[i] = aux2
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


def sentenceProcessing(text):
    sentences = text.split(';',1)
    print(sentences)
    senEn = []
    for sentence in sentences:
        #aux = translateText(lengin='es',lengout='en', text=sentence)
        #...... Probando otro traductor ............
        #aux = gosTranslateText(langin='es',langout='en', text=sentence)
        #print(aux)
        #print(sentence)
        #-------------------------------------------
        aux = minimizar(sentence)
        aux = deletePunt(text=aux)
        aux = deleteStop(text=aux, leng='english')
        aux = stemmingLemmatizer(aux)
        senEn.append(aux)
    return senEn


def getWordsText(text):
    sentences = text.split(';')
    words = []
    for sentence in sentences:
        #aux = translateText(lengin='es',lengout='en', text=sentence)

        # ...... Probando otro traductor ............
        #aux = gosTranslateText(langin='es', langout='en', text=sentence)
        # -------------------------------------------

        aux = minimizar(sentence)
        aux = deletePunt(text=aux)
        aux = deleteStop(text=aux, leng='english')
        aux = stemmingLemmatizer(aux)
        for i in aux:
            words.append(i)
    return words



def preProcessing(where, senEn, pn):
    if pn!=None:
        cql1 = countryEPO(country=pn)
        cql2 = ''
    for i in range(len(senEn)):
        if i == 0:
            aux = allEPO(where,senEn[i])
            if pn==None:
                cql1 = aux
            else:
                cql1 = andEPO(cql1,aux)
        elif i == 1:
            cql2 = anyEPO(where,senEn[i])
        else:
            aux = anyEPO(where,senEn[i])
            cql2 = andEPO(cql2,aux)
    if len(senEn)>1:
        return cql1+' and '+cql2
    else:
        return cql1


def getConcordance(words,abstract):
    text = nltk.tokenize.word_tokenize(str(abstract))
    freq = 0
    for i in range(len(words)):
        freq += (text.count(words[i])*100.0)/len(text)
    return freq


def getConcordancev2(words,abstract):
    text = nltk.tokenize.word_tokenize(str(abstract))
    freq = 0
    for i in words:
        for j in text:
            freq += similaridad(stemmingLemmatizer(i),stemmingLemmatizer(j))
    return freq


def Score(words, abstract,gamma):
    text = minimizar(abstract)
    text = deletePunt(text=text)
    text = deleteStop(text=text, leng='english')
    #text = nltk.tokenize.word_tokenize(text)
    text = deleteWord('CD',text)
    text = stemmingLemmatizer(text)

    #######################################################
    ##Pasar palabras de usuario y de abstract a vectores de modelo entrenado
    ######################################################
    words = list(set(words))
    text = list(set(text))
    v_usr =  np.zeros(len(model[words[1]]))
    for i in words:
        try:
            v_usr += model[i]
        except:
            print("%s -> en texto de usuario no es una palabra del vocabulario",i)

    v_usr = (1/len(words))*v_usr

    v_abs = np.zeros(len(model[words[1]]))
    for i in text:
        try:
            v_abs += model[i]
        except:
            print("%s -> en texto de abstract no es una palabra del vocabulario", i)
    v_abs = (1 / len(words))*v_abs

    similarity = 1 - scipy.spatial.distance.cosine(v_usr, v_abs)

    ##################################

    freq = list()
    freq_acum = 0
    score = 1
    for i in range(len(words)):
        freq_i = text.count(words[i])
        freq.append(freq_i)
        freq_acum += freq_i
        #print(freq_acum)
    for n in freq:
        if freq_acum==0:
            score = -math.inf
            score = 1
            return similarity*score
        else:
            aux = np.log(gamma+(n**(3/4))/(freq_acum**(3/4)))
            score += aux

    score = 1
    return similarity*score


def PCAScore(words, abstract,gamma):
    text = minimizar(abstract)
    text = deletePunt(text=text)
    text = deleteStop(text=text, leng='english')
    #text = nltk.tokenize.word_tokenize(text)
    text = deleteWord('CD',text)
    text = stemmingLemmatizer(text)

    #######################################################
    ##Pasar palabras de usuario y de abstract a vectores de modelo entrenado
    ######################################################

    alpha = 0.001
    v_usr =  np.zeros(len(model[words[1]]))
    for i in words:
        try:
            p = words.count(i)/len(words)
            k1 = (1/words.count(i))*alpha / (alpha + p)
            v_usr += k1*model[i]
        except:
            print(" En texto de usuario no es una palabra del vocabulario ->",i)

    v_usr = (1/len(words))*v_usr

    v_abs = np.zeros(len(model[words[1]]))
    for i in text:
        try:
            p = text.count(i)/len(text)
            k2 = (1 / text.count(i)) * alpha / (alpha + p)
            v_abs += k2*model[i]
        except:
            print(" En texto de abstract no es una palabra del vocabulario ->", i)
    v_abs = (1 / len(words))*v_abs

    similarity = 1 - scipy.spatial.distance.cosine(v_usr, v_abs)
    return similarity
    ##################################


def createCSV(text):
    name= './'+text+'.csv'
    outfile = open(name, 'w')
    #writer = csv.writer(outfile)
    #writer.writerow(["Frequency", "Pnumber", "Abstract"])


def writeCSV(text,freq,number,abstract):
    name= './'+text+'.csv'
    outfile = open(name, 'a')
    writer = csv.writer(outfile)
    writer.writerow([str(freq),number,abstract])


def sortCSV(path,name):
    df = pd.read_csv(path, names=["Frequency", "Pnumber", "Abstract"],dtype={'Frequency':'float64'})
    #df["Frequency"].convert_objects(convert_numeric=True)
    df = df.sort_values(["Frequency"],ascending=False)
    df.to_csv(name)
    #print(df.head())