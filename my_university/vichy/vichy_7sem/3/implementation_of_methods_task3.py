import numpy as np


def gaussian_elimination_with_determinant(n, matrix, epsilon):

    print("Исходная расширенная матрица системы:")
    print(matrix)

    det = 1.0
    matrix_A = np.copy(matrix[:, :-1])
    matrix_B = np.copy(matrix[:, -1])
    # Прямой ход
    for k in range(n):
        # Проверка малости ведущего элемента
        if abs(matrix[k, k]) < epsilon:
            print(f"Внимание: малый ведущий элемент на шаге {k+1}: {matrix[k, k]}")
            # return None, None, None

        # Деление строки на ведущий элемент
        det *= matrix[k, k]
        matrix[k, k + 1 :] = matrix[k, k + 1 :] / matrix[k, k]

        # Преобразование матрицы
        for i in range(k + 1, n):
            matrix[i, k + 1 :] -= matrix[i, k] * matrix[k, k + 1 :]

        # Вывод текущей матрицы после шага
        print(f"\nМатрица после шага {k+1} прямого хода:")
        print(matrix)

    # Обратный ход для нахождения решений
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = matrix[i, n] - np.sum(matrix[i, i + 1 : n] * x[i + 1 : n])

    # Вычисление невязки
    residual = matrix_A @ x - matrix_B

    # Выводы
    print("\nРешение системы (вектор x):")
    print(x)

    print("\nВектор невязки A*x - B:")
    print(residual)

    print("\nОпределитель det(A):")
    print(det)

    return x, residual, det


def gaussian_elimination_with_pivot_and_inverse_check(n, matrix, epsilon):

    print("Исходная расширенная матрица системы:")
    print(matrix)

    det = 1.0
    num_swaps = 0
    inverse_matrix = np.identity(n)  # Начальная единичная матрица для обратной матрицы
    matrix_A = np.copy(matrix[:, :-1])
    matrix_B = np.copy(matrix[:, -1])

    # Прямой ход с выбором главного элемента
    for k in range(n):
        # Выбор главного элемента по столбцу
        max_row = np.argmax(np.abs(matrix[k:, k])) + k
        if abs(matrix[max_row, k]) < epsilon:
            print(
                f"Внимание: малый ведущий элемент на шаге {k+1}: {matrix[max_row, k]}"
            )

        # Перестановка строк, если ведущий элемент не на текущей строке
        if max_row != k:
            matrix[[k, max_row]] = matrix[[max_row, k]]
            inverse_matrix[[k, max_row]] = inverse_matrix[[max_row, k]]
            num_swaps += 1
            print(f"Перестановка строк {k+1} и {max_row+1}")

        det *= matrix[k, k]

        factor = matrix[k, k]
        matrix[k, k + 1 :] /= factor
        inverse_matrix[k] /= factor

        # Преобразование матрицы и обновление обратной матрицы
        for i in range(k + 1, n):
            factor = matrix[i, k]
            matrix[i, k + 1 :] -= factor * matrix[k, k + 1 :]
            inverse_matrix[i] -= factor * inverse_matrix[k]

        # Вывод текущей матрицы после шага
        print(f"\nМатрица после шага {k+1} прямого хода:")
        print(matrix)

    # Обратный ход для нахождения решения
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = matrix[i, n] - np.sum(matrix[i, i + 1 : n] * x[i + 1 : n])

    # Обратный ход для обратной матрицы
    for i in range(n - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            factor = matrix[j, i]
            # matrix[j, i] -= factor * matrix[i, i]
            inverse_matrix[j] -= factor * inverse_matrix[i]

    # Корректировка определителя с учетом числа перестановок
    det *= (-1) ** num_swaps

    # Вычисление невязки
    residual = matrix_A @ x - matrix_B

    # Проверка обратной матрицы: A * A^-1
    identity_check = matrix_A @ inverse_matrix

    # Выводы
    print("\nРешение системы (вектор x):")
    print(x)

    print("\nВектор невязки A*x - B:")
    print(residual)

    print("\nОпределитель det(A):")
    print(det)

    print("\nОбратная матрица A^-1:")
    print(inverse_matrix)

    print(
        "\nРезультат умножения A на обратную матрицу (должна быть близка к единичной):"
    )
    print(identity_check)

    return x, residual, det, inverse_matrix, identity_check


def lu_decomposition_with_pivoting(n, A, epsilon):
    U = np.zeros((n, n))
    L = np.zeros((n, n))

    for i in range(n):
        for j in range(i, n):
            L[j, i] = A[j, i] - np.sum(L[j, :i] * U[:i, i])
        # max_row = np.argmax(np.abs(L[i:, i])) + i
        # if max_row != i:
        #     L[[i, max_row]] = L[[max_row, i]]
        for j in range(i, n):
            U[i, j] = (A[i, j] - np.sum(L[i, :i] * U[:i, j])) / L[i, i]

    return L, U


def lu_solve(L, U, B, n):

    # Решаем L*y = B
    y = np.zeros(n)
    for i in range(n):
        y[i] = (B[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

    # Решаем U*x = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - np.dot(U[i, i + 1 :], x[i + 1 :])

    return x


def LU_solve_and_print(n, matrix, epsilon):

    matrix_A = np.copy(matrix[:, :-1])
    matrix_B = np.copy(matrix[:, -1])
    L, U = lu_decomposition_with_pivoting(n, matrix[:, :-1], epsilon)

    # Вычисление вектора x
    x = lu_solve(L, U, matrix[:, -1], n)

    # Вычисление невязки
    residual = matrix_A @ x - matrix_B

    # Выводы
    print("\nНижнетреугольная матрица L")
    print(L)
    print("\nВерхнетреугольная матрица U")
    print(U)
    print("\nРезультат решения системы с помощью LU-разложения(вектор x)")
    print(x)
    print("\nВектор невязки")
    print(residual)
