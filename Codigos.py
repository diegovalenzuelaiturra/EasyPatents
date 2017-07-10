from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import csv
import pandas as pd
from nltk import pos_tag
#from BusquedasEPO import*


## Funciones para permutar
def inserta(x, lst, i):
    """Devuelve una nueva lista resultado de insertar
       x dentro de lst en la posicion i.
    """
    return lst[:i] + [x] + lst[i:]


def inserta_multiple(x, lst):
    """Devuelve una lista con el resultado de
       insertar x en todas las posiciones de lst.
    """
    return [inserta(x, lst, i) for i in range(len(lst) + 1)]


def permuta(lista):
    aux = []
    for i in range(len(lista)):
        b = lista[i]
        a = lista[:i]
        c = lista[i:]
        if b in a:
            a.remove(b)
        if b in c:
            c.remove(b)
        aux2 = list([b]+a+c)
        aux.append(aux2)
    return aux

## Funciones para preprocesar el texto
def minimizar(text):
    return text.lower()


def stemmingLemmatizer(text):
    ps = WordNetLemmatizer()
    aux1 = text
    for i in range(len(text)):
        aux2 = ps.lemmatize(aux1[i])
        aux1[i] = aux2
    return aux1



def deletePunt(text):
    return RegexpTokenizer(r'\w+').tokenize(text)


def deleteStop(leng, text):
    stop = set(stopwords.words(leng))
    aux = text
    for i in aux:
        if i in stop:
            aux.remove(i)
    return aux


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

## Funciones para el manejo de CSV
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
    df = df.sort_values(["Frequency"],ascending=False)
    df.to_csv(name)


def deleteWord(type,words):
    aux = list()
    sent = pos_tag(words)
    for i in sent:
        if i[1]==type:
            pass
        else:
            aux.append(i[0])
    return aux