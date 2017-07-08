import numpy as np
import pandas as pd
import seaborn as sns


def main():

    df = pd.read_csv('./TX_vec.csv')

    # La i-ésima fila de TX_vec (i.e. TX_vec[i]) corresponde a un vector transformado que representa a un abstract
    TX_vec = [ df.values[i][1:] for i in range(df.shape[0]) ]

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


if __name__ == '__main__':
    main()