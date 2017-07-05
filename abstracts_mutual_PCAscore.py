from BusquedasSem import *
import seaborn as sns


def main():

    df = pd.read_csv('./client0-sort.csv')
    df_abstract = df['Abstract']

    l = df_abstract.size
    abstracts = df_abstract.values

    PCA_score = np.zeros((l, l))

    abstracts_aux = preprocessing_abstracts_PCA(abstracts)

    for i in range(l):
        #PCA_score[i][:] = PCAscore2(thoughtobeat(words=abstracts_aux[i], abstracts=abstracts_aux))
        aux = PCAscore2(thoughtobeat(words=abstracts_aux[i], abstracts=abstracts_aux))
        for j in range(l):
            PCA_score[i][j] = aux[j]

    print(PCA_score)

    PCA_score = pd.DataFrame(PCA_score)

    sns.set()
    sns.heatmap(PCA_score)
    sns.plt.show()


def preprocessing_abstracts_PCA(abstracts):
    abstracts_aux = []
    for abstract in abstracts:
        text = minimizar(abstract)
        text = deletePunt(text=text)
        text = deleteStop(text=text, leng='english')
        #text = nltk.tokenize.word_tokenize(text)
        text = deleteWord('CD', text)
        text = deleteWord('DT', text)
        text = stemmingLemmatizer(text)
        abstracts_aux.append(text)
    return abstracts_aux





def simpleScore(abstract_i, abstract_j, gamma):

    freq = list()
    freq_acum = 0
    score = 1

    # (?) normalizar score por longitud del abstract (?)
    l_i = len(abstract_i)
    l_j = len(abstract_j)

    for i in abstract_i:
        for j in abstract_j:
            freq_i = abstract_j.count(i)/l_j
            freq_j = abstract_i.count(j)/l_i
            freq.append(freq_i+freq_j)
            freq_acum += freq_i+freq_j

    maximo = np.amax(freq)
    for n in freq:
        if freq_acum == 0:
            score = -math.inf
            return score
        else:
            aux = np.log(gamma+((n/maximo)**(3/4))/(freq_acum**(3/4)))
            score += aux
    return score


def Score_abstract_preprocessing(abstract):
    text = minimizar(abstract)
    text = deletePunt(text=text)
    text = deleteStop(text=text, leng='english')
    text = deleteWord('CD', text)
    text = stemmingLemmatizer(text)
    return text.split()


if __name__ == '__main__':
    main()
