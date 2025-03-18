import numpy as np


def create_matrix(a_diag, b_diag, c_diag, d_vector, n):
    matrix = np.zeros((n + 1, n + 1))  # создаем матрицу размером (n+1, n+1)
    # Проверка на диагональное преобладание
    for k in range(1, n):
        if abs(b_diag[k]) <= abs(a_diag[k]) + abs(c_diag[k]):
            raise Exception("Нарушено диагональное преобладание!")
    if abs(b_diag[0]) <= abs(c_diag[0]) or abs(b_diag[n]) <= abs(a_diag[n - 1]):
        raise Exception("Нарушено диагональное преобладание!")
    # Заполнение главной диагонали
    np.fill_diagonal(matrix, b_diag)

    # Заполнение поддиагонали (ниже главной диагонали)
    for i in range(1, n + 1):
        matrix[i, i - 1] = a_diag[i - 1]

    # Заполнение наддиагонали (выше главной диагонали)
    for i in range(n):
        matrix[i, i + 1] = c_diag[i]

    # Преобразование вектора d в столбец
    d_vector = d_vector.reshape(-1, 1)

    # Объединяем матрицу и вектор
    augmented_matrix = np.hstack([matrix, d_vector])

    # print("Расширенная матрица:")
    # print(augmented_matrix)
    return augmented_matrix


def solve_lin_sys(all_matrix, n):
    m_vector = np.zeros(n + 1)
    l_vector = np.zeros(n + 1)
    y_ans_vector = np.zeros(n + 1)

    # Прямой ход метода прогонки
    m_vector[1] = -all_matrix[0, 1] / all_matrix[0, 0]
    l_vector[1] = all_matrix[0, n + 1] / all_matrix[0, 0]

    for i in range(1, n):
        denominator = all_matrix[i, i - 1] * m_vector[i] + all_matrix[i, i]
        m_vector[i + 1] = -all_matrix[i, i + 1] / denominator
        l_vector[i + 1] = (
            all_matrix[i, n + 1] - all_matrix[i, i - 1] * l_vector[i]
        ) / denominator

    # Обратный ход
    y_ans_vector[n] = (all_matrix[n, n + 1] - all_matrix[n, n - 1] * l_vector[n]) / (
        all_matrix[n, n - 1] * m_vector[n] + all_matrix[n, n]
    )
    for k in range(n - 1, -1, -1):
        y_ans_vector[k] = m_vector[k + 1] * y_ans_vector[k + 1] + l_vector[k + 1]

    # Вычисление нормы невязки с учетом трехдиагонального вида
    # residual = np.zeros(n + 1)
    # residual[0] = (
    #     all_matrix[0, 0] * y_ans_vector[0]
    #     + all_matrix[0, 1] * y_ans_vector[1]
    #     - all_matrix[0, n + 1]
    # )
    # for i in range(1, n):
    #     residual[i] = (
    #         all_matrix[i, i - 1] * y_ans_vector[i - 1]
    #         + all_matrix[i, i] * y_ans_vector[i]
    #         + all_matrix[i, i + 1] * y_ans_vector[i + 1]
    #         - all_matrix[i, n + 1]
    #     )
    # residual[n] = (
    #     all_matrix[n, n - 1] * y_ans_vector[n - 1]
    #     + all_matrix[n, n] * y_ans_vector[n]
    #     - all_matrix[n, n + 1]
    # )

    # # Норма вектора невязки
    # residual_norm = np.linalg.norm(residual, ord=np.inf)
    # print("Норма вектора невязки:", residual_norm)

    return y_ans_vector
