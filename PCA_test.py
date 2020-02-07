from BusquedasSem import *
import pandas as pd
import seaborn as sns


def main():

    df = pd.read_csv('./client0-sort.csv')
    abstracts = df['Abstract'].values

    #    abstracts_aux = abstracts

    abstracts_aux = []
    for abstract in abstracts:
        text = minimizar(abstract)
        text = deletePunt(text=text)
        text = deleteStop(text=text, leng='english')
        #text = nltk.tokenize.word_tokenize(text)
        text = deleteWord('CD', text)
        text = stemmingLemmatizer(text)
        abstracts_aux.append(text)
    print(abstracts_aux[0])

    words = getWordsText(
        'explosive emulsion; plastic explosive; oil with water; robust')

    X = thoughtobeat(words=words, abstracts=abstracts_aux)
    pca_score = PCAscore2(X)

    print(pca_score)

    df_pca_score = pd.DataFrame(pca_score, columns=['PCA Score'])
    df_abstracts = pd.DataFrame(abstracts, columns=['Abstract'])
    df_pca_abstracts = pd.concat([df_pca_score, df_abstracts], axis=1)

    df = df_pca_abstracts.sort_values(['PCA Score'], ascending=False)
    df.to_csv('PCA_Sorted_Abstracts1.csv')


if __name__ == '__main__':
    main()
