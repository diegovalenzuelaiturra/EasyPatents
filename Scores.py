import scipy
from math import*
from Codigos import*
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
from GensimFun import*

googleNew = '../glove.6B.300d.txt'
wiki400 = '../wiki.6B.300d.txt'
model = loadModel(wiki400,False)

def thoughtobeat(words, abstracts):
    #Basado en artículo: though to beat baseline for sentence embeddings
    #Input: Words debe ser array de palabras que componen palabras que ingresó usuario
    #Abstracts debe ser un array donde cada elemento es un abstract. Cada abstract debe ser un array de palabras del abstract
    #Output: matriz que contiene vectores de usuario y abstracts sin la componente principal

    X_vec = []
    alpha = 0.001

    v_usr, vectores = Crearvectores2(words, abstracts, alpha)
    X_vec.append(v_usr)
    for v_abs in vectores:
        X_vec.append(v_abs)
    TX_vec = Restarcomponente(X_vec)
    return TX_vec


def Crearvectores(palabras, alpha):
    #Input: array de oración cuyos elementos son palabras
    #Output: vector de word2vec creado en base a artículo "Though to beat baseline for sentence embeddings"

    v_usr = np.zeros(len(model['man']))
    for i in palabras:
        try:
            p = palabras.count(i) / len(palabras)
            k1 = (1 / palabras.count(i)) * alpha / (alpha + p)
            v_usr += k1 * model[i]
        except:
            pass
            #print(" En texto de usuario no es una palabra del vocabulario ->", i)

    v_usr = (1 / len(palabras)) * v_usr
    return v_usr


def Crearvectores2(words, oraciones, alpha):
    ##Input: words es array de palabras ingresadas por usuario
    ## oraciones es array de abstracts, cada abstract es array de palabras
    ## alfa es parametro de though to beat
    ##Output: v_usr = vector de words y vectores = array de vectores de abstracts
    L=0
    for oracion in oraciones:
        L += len(oracion)

    v_usr = np.zeros(len(model['man']))
    for i in words:
        try:
            total_i = np.sum([oraciones[x].count(i) for x in range(len(oraciones))])
            p = total_i/L #oraciones.count(i) / L
            k1 = (1 / words.count(i)) * alpha / (alpha + p)
            v_usr += k1 * model[i]
        except:
            pass
            #print(" En texto de usuario no es una palabra del vocabulario ->", i)

    vectores = []
    for oracion in oraciones:
        v = np.zeros(len(model['man']))
        for i in oracion:
            try:
                total_i = np.sum([oraciones[x].count(i) for x in range(len(oraciones))])
                p = total_i/L #oraciones.count(i) / L
                k1 = (1 / total_i) * alpha / (alpha + p)
                v += k1 * model[i]
            except:
                print(" En texto de abstract no es una palabra del vocabulario ->", i)
                pass
        vectores.append(v)
    return v_usr, vectores


def Restarcomponente(X):
    #Función que toma una matriz cuyas filas son vectores de oraciones, se le aplica transformación de "Though to beat baseline..."
    #Input: Array cuyos elementos son arrays.
    #Output: Matriz a la que se le ha aplicado transformación
    pca = doPCA(X)
    TX = []
    for vec in X:
        TX.append(vec - pca.components_[0] * np.dot(vec, pca.components_[0]))
    return TX


def PCAscore2(TX_vec):
    v_usr = TX_vec[0][:]
    #print(v_usr)
    puntajes=[]

    for vec in TX_vec:
        puntaje = 1 - scipy.spatial.distance.cosine(v_usr, vec)
        #print(puntaje)
        puntajes.append(puntaje)
    #print(puntajes)
    puntajes.pop(0)
    #print(puntajes)
    return puntajes


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


def doPCA(X):
    pca = PCA(n_components=1)
    pca.fit(X)
    return pca


def thoughtobeat2(abstracts):
    #Basado en artículo: though to beat baseline for sentence embeddings
    #Input: Abstracts debe ser un array donde cada elemento es un abstract. Cada abstract debe ser un array de palabras del abstract
    #Output: matriz que contiene vectores de abstracts sin la componente principal

    X_vec = []
    alpha = 0.001

    v_usr, vectores = Crearvectores2(abstracts[0], abstracts, alpha)
    for v_abs in vectores:
        X_vec.append(v_abs)
    TX_vec = Restarcomponente(X_vec)
    return TX_vec


def mutualScoreAbs(df_abstract,path):
    l = df_abstract.size
    abstracts = df_abstract.values

    PCA_score = np.zeros((l, l))

    abstracts_aux = preprocessing_abstracts_PCA(abstracts)

    for i in range(l):
        aux = PCAscore2(thoughtobeat(words=abstracts_aux[i], abstracts=abstracts_aux))
        for j in range(l):
            PCA_score[i][j] = aux[j]

    PCA_score = pd.DataFrame(PCA_score)
    sns.set()
    plt = sns.heatmap(PCA_score)
    fig = plt.get_figure()
    fig.savefig(path+".png")
    #sns.plt.show()


def preprocessing_abstracts_PCA(abstracts):
    abstracts_aux = []
    for abstract in abstracts:
        text = preprocessingText(str(abstract))
        abstracts_aux.append(text)
    return abstracts_aux


def ScoreTextToAbstract(text,abstracts):
    abstracts_aux = preprocessing_abstracts_PCA(abstracts)
    text_aux = preprocessingText(text)
    PCA_score = PCAscore2(thoughtobeat(words=text_aux, abstracts=abstracts_aux))
    return PCA_score


def preprocessingText(abstract):
    text = minimizar(abstract)
    text = deletePunt(text=text)
    text = deleteStop(text=text, leng='english')
    # text = nltk.tokenize.word_tokenize(text)
    text = deleteWord('CD', text)
    text = deleteWord('DT', text)
    text = stemmingLemmatizer(text)
    return text