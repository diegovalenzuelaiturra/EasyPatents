from BusquedasSem import *
import seaborn as sns


def main():

    df = pd.read_csv('./client0-sort.csv')
    abstracts = df['Abstract']

    #l = abstracts.size
    l = 32 # quiero plotear algunos pocos no más
    score = np.zeros((l, l))
    simple_score = np.zeros((l, l))

    for i in range(score.shape[0]):
        for j in range(score.shape[1]):

            # score usando word2vec
            #score[i][j] = Score(words=Score_abstract_preprocessing(abstracts[i]),
            #                    abstract=Score_abstract_preprocessing(abstracts[j]),
            #                    gamma=0.1)

            # score sin usar word2vec
            simple_score[i][j] = simpleScore(abstract_i=Score_abstract_preprocessing(abstracts[i]),
                                             abstract_j=Score_abstract_preprocessing(abstracts[j]),
                                             gamma=0.1)

    #simple_score = sigmoid(simple_score)


    sns.set()

    # score usando word2vec
    # sns.heatmap(score)
    # sns.plt.show()

    # score sin usar word2vec
    sns.heatmap(simple_score)
    sns.plt.show()

def sigmoid(x):
    return 1/(1 + np.exp(-x))

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
