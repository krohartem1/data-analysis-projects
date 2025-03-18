import numpy as np


def lu_decomposition_with_pivoting_inplace(A, epsilon=1e-12):
    n = A.shape[0]
    P = np.eye(n)

    for j in range(n):

        pivot_index = j + np.argmax(np.abs(A[j:, j]))
        if np.abs(A[pivot_index, j]) < epsilon:
            print(f"Внимание: малый ведущий элемент на шаге {j+1}: {A[pivot_index, j]}")

        if pivot_index != j:
            A[[j, pivot_index], :] = A[[pivot_index, j], :]
            P[[j, pivot_index], :] = P[[pivot_index, j], :]

        for i in range(j + 1, n):
            A[i, j] /= A[j, j]
            for k in range(j + 1, n):
                A[i, k] -= A[i, j] * A[j, k]

    return P, A


def extract_L_U(A):
    n = A.shape[0]
    L = np.tril(A, -1)
    L += np.diag(np.diag(A))
    U = np.triu(A)
    np.fill_diagonal(U, 1)
    return L, U


def lu_solve_inplace(P, A, B):
    n = A.shape[0]

    B_permuted = np.dot(P, B)

    y = np.zeros_like(B_permuted)
    for i in range(n):
        y[i] = B_permuted[i] - np.dot(A[i, :i], y[:i])

    x = np.zeros_like(y)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(A[i, i + 1 :], x[i + 1 :])) / A[i, i]

    return x


def main():

    # matrix = np.array(
    #     [
    #         [6.5176e-06, -8.0648e-03, 4.23528, 3.61628],
    #         [5.9176e-03, -0.80648, 1.46528, 1.52097],
    #         [0.87176, 0.79352, 0.91528, 1.81150],
    #     ],
    #     dtype=float,
    # )
    matrix = np.array(
        [
            [6.9880e-06, -7.1240e-03, 4.37640, 3.99895],
            [6.3880e-03, -0.71240, 1.60640, 1.77052],
            [0.91880, 0.88760, 1.05640, 2.12361],
        ],
        dtype=float,
    )
    A_orig = np.copy(matrix[:, :-1])
    A = matrix[:, :-1].copy()
    B = matrix[:, -1].copy()

    P, A_lu = lu_decomposition_with_pivoting_inplace(matrix[:, :-1])

    L, U = extract_L_U(A_lu)

    print("Матрица перестановок P:")
    print(P)
    print("\nНижнетреугольнвая матрица L:")
    print(L)
    print("\nВерхнетреугольная матрица U:")
    print(U)

    x = lu_solve_inplace(P, A_lu, B)
    print("\nВектор решение x:")
    print(x)

    residual = A @ x - B
    print("\nResidual vector A * x - B:")
    print(residual)


main()
