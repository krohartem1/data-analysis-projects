import numpy as np


def create_matrix(n):
    matrix = np.zeros((n + 1, n + 1))  # создаем матрицу размером (n+1, n+1)
    all = ()
    with open("task1.txt", "r") as inp:
        for line in inp:
            all += (line.strip(),)
    a_diag = np.array([float(i) for i in all[0].split()])

    b_diag = np.array([float(i) for i in all[1].split()])

    c_diag = np.array([float(i) for i in all[2].split()])

    d_vector = np.array([float(i) for i in all[3].split()])

    # Проверка на диагональное преобладание
    for k in range(1, n):
        if abs(b_diag[k]) <= abs(a_diag[k]) + abs(c_diag[k]):
            raise Exception("Нарушено диагональное преобладание!")
        elif abs(b_diag[0]) <= abs(c_diag[0]) or abs(b_diag[n]) <= abs(a_diag[n - 1]):
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


def solve_lin_sys(all_matrix, n, y_ans_vector):
    m_vector = np.zeros(n + 1)
    l_vector = np.zeros(n + 1)
    m_vector[1] = -all_matrix[0, 1] / all_matrix[0, 0]
    l_vector[1] = all_matrix[0, n + 1] / all_matrix[0, 0]
    for i in range(1, n):
        m_vector[i + 1] = -all_matrix[i, i + 1] / (
            all_matrix[i, i - 1] * m_vector[i] + all_matrix[i, i]
        )
        if m_vector[i + 1] > 1:
            print("Ошибка может расти, обратите внимание на номер ", i + 1)
        l_vector[i + 1] = (
            all_matrix[i, n + 1] - all_matrix[i, i - 1] * l_vector[i]
        ) / (all_matrix[i, i - 1] * m_vector[i] + all_matrix[i, i])
    print("Прогоночные коэффициенты")
    print("Вектор m:", end=" ")
    print(m_vector[1:])
    print("Вектор l:", end=" ")
    print(l_vector[1:])
    # y_ans_vector = np.zeros(n + 1)
    y_ans_vector[n] = (all_matrix[n, n + 1] - all_matrix[n, n - 1] * l_vector[n]) / (
        all_matrix[n, n - 1] * m_vector[n] + all_matrix[n, n]
    )
    for k in range(n, 0, -1):
        y_ans_vector[k - 1] = m_vector[k] * y_ans_vector[k] + l_vector[k]
    print("Вектор ответ:", end=" ")
    print(y_ans_vector)
    print("Норма вектора невязки:", end=" ")
    print(
        np.linalg.norm(
            all_matrix[0 : n + 1, 0 : n + 1] @ y_ans_vector - all_matrix[:, n + 1],
            ord=np.inf,
        )
    )


# solve_lin_sys(create_matrix(n))
