import tridiag_matrix_task2 as tm2
import numpy as np


# Функция для явной схемы
def explicit_scheme(N, T, tau, f, u_exact, phi, alpha, beta):
    h = 1 / N  # шаг по пространству
    if tau > float(h**2 / 2):
        tau = float(h**2 / 2)
    M = int(T / tau)  # количество временных слоев
    sigma = tau / h**2  # коэффициент

    # Создаем сетку
    x_grid = np.linspace(0, 1, N + 1)
    t_grid = np.linspace(0, T, M + 1)
    u = np.zeros((M + 1, N + 1))

    u[0, :] = phi(x_grid)  # начальное условие

    # Применяем явную схему
    # Граничные условия
    u[1:, 0] = alpha(t_grid[1:])
    u[1:, N] = beta(t_grid[1:])

    # F = np.array([[f(x, t) for x in x_grid] for t in t_grid])

    # # Обновляем значения внутри области
    u[1:, 1:N] = (
        u[:M, 1:N]
        + sigma * (u[:M, 0 : N - 1] - 2 * u[:M, 1:N] + u[:M, 2:])
        + tau * f(x_grid[1:N], t_grid[:M, None])
    )

    u_true = np.array([[u_exact(x, t) for x in x_grid] for t in t_grid])

    # Вычисляем максимальное отклонение от точного решения
    max_error = np.max(np.abs(u - u_true))
    return u, max_error


# Функция для неявной схемы
def implicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta, solve_lin_sys, create_matrix
):
    h = 1 / N  # шаг по пространству
    M = int(T / tau)  # количество временных слоев
    sigma = tau / h**2  # коэффициент

    x_grid = np.linspace(0, 1, N + 1)
    t_grid = np.linspace(0, T, M + 1)
    u = np.zeros((M + 1, N + 1))
    u[0, :] = phi(x_grid)

    max_residual_norms = []
    for n in range(M):
        d_vector = np.zeros(N + 1)

        # Граничные условия
        d_vector[0] = alpha(t_grid[n + 1])
        d_vector[N] = beta(t_grid[n + 1])

        # Внутренние узлы
        for j in range(1, N):
            d_vector[j] = u[n, j] + tau * f(x_grid[j], t_grid[n])

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
        u_next, residual_norm = solve_lin_sys(all_matrix, N)
        # max_residual_norms.append(residual_norm)

        # Обновляем значения на следующем временном слое
        u[n + 1, :] = u_next

    # max_residual = np.max(max_residual_norms)
    u_true = u_exact(t_grid[:, None], x_grid[None, :])
    # print(f"{np.isnan(u).any()=}")
    max_error = np.max(np.abs(u - u_true))
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


# Входные параметры
# N = int(input("Введите количество разбиений N: "))
# T = float(input("Введите конечное время T: "))
# tau = float(input("Введите шаг по времени τ: "))

# Решение задачи явной схемой
N = 100
T = 1
tau = 0.01
u_explicit, max_error_explicit = explicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta
)
print("Максимальная ошибка для явной схемы:", max_error_explicit)

print(np.isnan(u_explicit).any())
# Решение задачи неявной схемой
u_implicit, max_error_implicit = implicit_scheme(
    N, T, tau, f, u_exact, phi, alpha, beta, tm2.solve_lin_sys, tm2.create_matrix
)
print("Максимальная ошибка для неявной схемы:", max_error_implicit)
