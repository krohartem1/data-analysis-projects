import tridiag_matrix_task2 as tm2
import numpy as np


# Функция для явной схемы
def explicit_scheme(N, T, tau, f, u_exact, phi, alpha, beta):
    h = 1 / N  # шаг по пространству
    if tau > float(h**2 / 2):
        tau = float(h**2 / 2)
        print(f"tau будет изменен и равен = {tau}")
    if tau * h < 10 ** (-7):
        raise Exception("!Слишком маленькое дробление, долгий счет!")

    M = int(T / tau)  # количество временных слоев
    sigma = tau / h**2  # коэффициент

    # Создаем сетку
    x_grid = np.linspace(0, 1, N + 1)
    t_grid = np.linspace(0, T, M + 1)
    u = np.zeros((N + 1, M + 1))
    u[:, 0] = phi(x_grid)  # начальное условие

    # Применяем явную схему
    for m in range(M):
        # Граничные условия
        u[0, m + 1] = alpha(t_grid[m + 1])
        u[N, m + 1] = beta(t_grid[m + 1])

        # Обновляем значения внутри области
        for j in range(1, N):
            u[j, m + 1] = (
                u[j, m]
                + sigma * (u[j - 1, m] - 2 * u[j, m] + u[j + 1, m])
                + tau * f(x_grid[j], t_grid[m])
            )
    u_true = np.array([[u_exact(x, t) for t in t_grid] for x in x_grid])
    # Вычисляем максимальное отклонение от точного решения
    max_error = np.max(np.abs(u - u_true))

    # Выводы
    print("\nКоличество временных слоев = ", M)
    print("\nh = ", h)
    print(f"\n Теоретическая погрешность = {tau + h**2}")
    return u, max_error, tau


# Функция для неявной схемы
def implicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta, solve_lin_sys, create_matrix
):
    h = 1 / N  # шаг по пространству
    M = int(T / tau)  # количество временных слоев
    sigma = tau / h**2  # коэффициент

    x_grid = np.linspace(0, 1, N + 1)
    t_grid = np.linspace(0, T, M + 1)
    u = np.zeros((N + 1, M + 1))
    u[:, 0] = phi(x_grid)

    max_residual_norms = []
    for m in range(M):
        d_vector = np.zeros(N + 1)

        # Граничные условия
        d_vector[0] = alpha(t_grid[m + 1])
        d_vector[N] = beta(t_grid[m + 1])

        # Внутренние узлы
        for j in range(1, N):
            d_vector[j] = u[j, m] + tau * f(x_grid[j], t_grid[m])

        # Коэффициенты для трехдиагональной матрицы
        a_diag = np.full(N, -sigma)
        b_diag = np.full(N + 1, 1 + 2 * sigma)
        c_diag = np.full(N, -sigma)

        # Заменяем первую и последнюю диагонали на 1 для учета граничных условий
        b_diag[0] = 1
        b_diag[N] = 1
        c_diag[0] = 0
        a_diag[N - 1] = 0
        # Формируем матрицу
        all_matrix = create_matrix(a_diag, b_diag, c_diag, d_vector, N)

        # Решаем систему
        u_next = solve_lin_sys(all_matrix, N)

        # Обновляем значения на следующем временном слое
        u[:, m + 1] = u_next

    # max_residual = np.max(max_residual_norms)
    max_error = np.max(np.abs(u - u_exact(x_grid[:, None], t_grid[None, :])))
    print(f"tau = {tau}")
    print("\nКоличество временных слоев = ", M)
    print("\nh = ", h)
    print(f"\n Теоретическая погрешность = {tau + h**2}")
    return u, max_error


# Определение исходных функций задачи
def u_exact(x, t):
    # return np.exp(-4 * t) * np.sin(2 * x) + np.exp(-t) * (1 - x) ** 2
    return np.exp(-0.25 * t) * (np.sin(0.5 * x) + 1 - x)


def f(x, t):
    # return np.exp(-t) * (x**2 - 3)
    return -0.25 * np.exp(-0.25 * t) * (1 - x)


def phi(x):
    # return np.sin(2 * x) + 1 - x**2
    return np.sin(0.5 * x) + 1 - x


def alpha(t):
    # return np.exp(-t)
    return np.exp(-0.25 * t)


def beta(t):
    # return np.exp(-4 * t) * np.sin(2)
    return np.exp(-0.25 * t) * np.sin(0.5)


# Решение задачи явной схемой
N = 100
T = 1
tau = 0.01
print("Явная трехточечная")
u_explicit, max_error_explicit, tau = explicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta
)
print("Максимальная ошибка для явной схемы:", max_error_explicit)

print("_____________________\n\n")
# Решение задачи неявной схемой
print("Неявная трехточечная")
u_implicit, max_error_implicit = implicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta, tm2.solve_lin_sys, tm2.create_matrix
)
print("Максимальная ошибка для неявной схемы:", max_error_implicit)
