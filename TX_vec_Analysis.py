import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def main():

    df = pd.read_csv('./TX_vec.csv')

    # La i-ésima fila de TX_vec (i.e. TX_vec[i]) corresponde a un vector transformado que representa a un abstract
    TX_vec = [ df.values[i][1:] for i in range(df.shape[0]) ]

    f = open('TX_vec.tsv', 'w')
    for i in range(len(TX_vec)):
        for j in range(len(TX_vec[1])):
            f.write(str(TX_vec[i][j]) + '\t')
        f.write('\n')

#   SVD
#   https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.svd.html

#   full_matrices: bool, optional
#   If True (default), u and v have the shapes (M, M) and (N, N), respectively.
#   Otherwise, the shapes are (M, K) and (K, N), respectively, where K = min(M, N).

    U, s, V = np.linalg.svd(TX_vec, full_matrices=True, compute_uv=True)

    S = np.zeros((U.shape[1], V.shape[0]), dtype=float)
    S[:s.shape[0], :s.shape[0]] = np.diag(s) # Matriz Diagonal de Valores Propios ordenados


    print('SVD shapes' +
          '\n U shape = ' + str(U.shape) +
          '\n V shape = ' + str(V.shape) +
          '\n s shape = ' + str(s.shape) +
          '\n S shape = ' + str(S.shape)
          )

#   Reconstruction
    USV = np.dot(U, np.dot(S, V))
    # print(USV)


########################################################################################################################

# USELESS

#   http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html #sphx-glr-auto-examples-cluster-plot-dbscan-py

#   eps = 5
#   eps = 25

    X = TX_vec
    X = StandardScaler().fit_transform(X)
    db = DBSCAN(eps=15, min_samples=3).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))


    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

########################################################################################################################


if __name__ == '__main__':
    main()