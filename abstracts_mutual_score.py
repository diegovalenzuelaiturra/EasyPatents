from BusquedasSem import *
import seaborn as sns
import pandas as pd

def main():

    df = pd.read_csv('./PCA_Sorted_Abstracts1.csv')
    abstracts = df['Abstract'].values
    l = df['Abstract'].size
    score = np.zeros((l, l))

    TX_vec = thoughtobeat2(abstracts=abstracts)

    for i in range(l):
        for j in range(l):
            score[i][j] = 1 - scipy.spatial.distance.cosine(TX_vec[i][:], TX_vec[j][:])

    sns.set()
    sns.heatmap(score)
    sns.plt.show()

    df_mutual_pca_score = pd.DataFrame(score)
    df_mutual_pca_score.to_csv('SORTED_Abstracts_Mutual_PCA_Score1.csv')


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
