from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re
import datetime

## Librerias para operar con diccionarios
from collections import defaultdict
import operator

## Librerias para el manejo con vectores
import gensim
import numpy as np
import scipy

#Librerias para escribir el csv
import csv

#Librerias para enviar correo
from EPmail import *


wiki400 = '../glove.6B/wiki.txt'
model = gensim.models.KeyedVectors.load_word2vec_format(wiki400, binary=False)

def makevector(palabras):
    v_usr = np.zeros(len(model['man']))
    for i in palabras:
        try:
            v_usr += model[i]
        except:
            pass
    if len(palabras) == 0:
        v_usr = (1 / 1e-8) * v_usr
    else:
        v_usr = (1 / len(palabras)) * v_usr
    return v_usr#,v_vec


def minimizar(text):
    return text.lower()


def delete_puntuation(text):
    return RegexpTokenizer(r'\w+').tokenize(text)


def getWords(text):
    sentences = text.split()
    words = []
    for sentence in sentences:
        aux = minimizar(sentence)
        aux = delete_puntuation(text=aux)
        aux = deleteStop(text=aux)
        aux = stemmingLemmatizer(aux)
        for i in aux:
            if i not in words:
                words.append(i)
    return words


def deleteStop(lang='english', text=['']):
    stop = set(stopwords.words(lang))
    aux = text
    for i in aux:
        if i in stop:
            aux.remove(i)
    return aux


def stemmingLemmatizer(text):
    ps = WordNetLemmatizer()
    aux1 = text
    for i in range(len(text)):
        aux2 = ps.lemmatize(aux1[i])
        aux1[i] = aux2
    return aux1


def generateIPC(responses):
    d = defaultdict(int)
    for response in responses:
        ipc = response[3].split('|')
        for i in ipc:
            ipc_class = i.split('/')[0]
            d[ipc_class] += 1

    ## Elegimos las primeras 5 categorias
    #return max(d.items(), key=operator.itemgetter(1))[0]
    return sorted(d.items(), key=operator.itemgetter(1), reverse=True)


def topK_IPC(sorted_d, k):
    sorted_IPC = []
    n = k if len(sorted_d) > k else len(sorted_d)
    for i in range(n):
        sorted_IPC.append(sorted_d[i][0])
    return sorted_IPC


def makeCSV(id, responses, description):
    path = str(id) + '.csv'
    write_file = open(path, 'w+')
    writer = csv.writer(write_file, delimiter=';')

    words = getWords(description)
    vector0 = makevector(words)
    for response in responses:
        publication_number = response[1]
        publication_date = response[2]
        applicant = re.sub(r'[^\x00-\x7f]',r' ',response[4])
        applicant = applicant.replace(';',',')
        inventor = re.sub(r'[^\x00-\x7f]',r' ',response[5])
        inventor = inventor.replace(';',',')
        abstract = re.sub(r'[^\x00-\x7f]',r' ',response[6])
        abstract = abstract.replace(';',',')
        title = re.sub(r'[^\x00-\x7f]',r' ',response[7])
        title = title.replace(';',',')
        vector = np.fromstring(response[8], dtype=np.float, sep=';')
        score = similarity(vector0,vector)
        writer.writerow([score,publication_number,publication_date, abstract, title, applicant, inventor])

    file_name = str(id) + '.csv'
    ifile = open(file_name, 'r')
    infile = csv.reader(ifile, delimiter=';')
    # create the sorted list
    sortedlist = sorted(infile, key=operator.itemgetter(0), reverse=True)
    ifile.close()

    # open the output file - it can be the same as the input file
    ofile_name = str(id) + '_sort.csv'
    ofile = open(ofile_name, 'a')
    outfile = csv.writer(ofile, delimiter=';')
    # write the sorted list
    for row in sortedlist:
        outfile.writerow(row)

    return True


def convert(types, values):
    return [t(v) for t, v in zip(types, values)]


def date(s):
    return datetime.strptime(s, '%y-%m-%d')


def similarity(vector0, vector):
    similarity = 1 - scipy.spatial.distance.cosine(vector0, vector)
    return similarity


def correo(id, mail, respuesta):
    itext = "Estimad@, \n respondo a lo que solicito usando las palabras ["
    ftext = """\n Cualquier duda por favor contacta a patents@easypatents.cl \n Saludos Cordiales"""

    msubject = 'Vigilancia Tecnologica EasyPatents'
    mfrom = 'ro-bot@easypatents.cl'

    epm = EPmail()
    fname = './Report/main.pdf'
    fformat = './' + 'client'+str(id)+ '-report.pdf'
    mmessage = itext + respuesta + ' ] ' + ftext
    aux = epm.send_complex_message(mail,mfrom,msubject,mmessage,fformat,fname)
    print(aux)