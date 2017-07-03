from BusquedasSem import *
import seaborn as sns


def main():

    df = pd.read_csv('./resp.csv')
    abstracts = df['Abstract']

    #l = abstracts.size
    l = 32 # quiero plotear algunos pocos no más
    score = np.zeros((l, l))
    simple_score = np.zeros((l, l))

    for i in range(score.shape[0]):
        for j in range(score.shape[1]):

            # score usando word2vec
            score[i][j] = Score(words=getWordsText(abstracts[i]), abstract=abstracts[j], gamma=0.1)

            # score sin usar word2vec
            simple_score[i][j] = simpleScore(words=getWordsText(abstracts[i]), abstract=abstracts[j], gamma=0.1)

    sns.set()

    # score usando word2vec
    sns.heatmap(score)
    sns.plt.show()

    # score sin usar word2vec
    sns.heatmap(simple_score)
    sns.plt.show()


def simpleScore(words, abstract, gamma):
    text = Score_abstract_preprocessing(abstract)

    freq = list()
    freq_acum = 0
    score = 1

    # (?) normalizar score por longitud del abstract (?)

    for i in range(len(words)):
        freq_i = text.count(words[i])
        freq.append(freq_i)
        freq_acum += freq_i

    for n in freq:
        if freq_acum == 0:
            score = -math.inf
            return score
        else:
            aux = np.log(gamma+(n**(3/4))/(freq_acum**(3/4)))
            score += aux
    return score


def Score_abstract_preprocessing(abstract):
    text = minimizar(abstract)
    text = deletePunt(text=text)
    text = deleteStop(text=text, leng='english')
    text = deleteWord('CD', text)
    text = stemmingLemmatizer(text)

    return text


if __name__ == '__main__':
    main()
