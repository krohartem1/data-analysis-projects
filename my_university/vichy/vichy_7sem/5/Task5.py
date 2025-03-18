import numpy as np
from scipy import linalg
import pandas as pd


pd.options.display.float_format = "{:,.16f}".format
np.set_printoptions(precision=16, suppress=True)


def solve_power_method(a: np.ndarray, eps: float) -> (float, np.ndarray, int):

    eigenvector = np.random.rand(a.shape[1])
    eigenvector = eigenvector / linalg.norm(eigenvector)
    prev_eigenvector = eigenvector
    eigenvalue = 0
    prev_eigenvalue = None
    counter = 0

    while prev_eigenvalue is None or abs(eigenvalue - prev_eigenvalue) >= eps:
        prev_eigenvector = eigenvector
        prev_eigenvalue = eigenvalue
        eigenvector = a @ eigenvector
        eigenvalue = eigenvector[0] / prev_eigenvector[0]
        eigenvector = eigenvector / linalg.norm(eigenvector)
        counter += 1

    return eigenvalue, eigenvector, counter


def solve_dot_product_method(a: np.ndarray, eps: float) -> (float, np.ndarray, int):

    eigenvector = np.random.rand(a.shape[1])
    eigenvector = eigenvector / linalg.norm(eigenvector)

    helper_eigenvector = np.random.rand(a.shape[1])
    helper_eigenvector = helper_eigenvector / linalg.norm(helper_eigenvector)

    prev_eigenvalue = None
    eigenvalue = 0
    counter = 0

    while prev_eigenvalue is None or abs(eigenvalue - prev_eigenvalue) >= eps:
        prev_eigenvalue = eigenvalue
        eigenvector = a @ eigenvector
        eigenvector = eigenvector / linalg.norm(eigenvector)
        eigenvalue = np.dot(eigenvector, a @ eigenvector) / np.dot(
            eigenvector, eigenvector
        )
        # helper_eigenvector = a.T @ helper_eigenvector
        # helper_eigenvector = helper_eigenvector / linalg.norm(helper_eigenvector)
        counter += 1

    return eigenvalue, eigenvector, counter


def find_opposite_spectral_bound(
    a: np.ndarray, eps: float = 1e-10
) -> (float, np.ndarray):
    lambda1, eigenvector1, _ = solve_power_method(a, eps)
    b = a - lambda1 * np.eye(a.shape[0])
    lambda_b, eigenvector_b, _ = solve_power_method(b, eps)
    lambda_opposite = lambda_b + lambda1
    return lambda_opposite, eigenvector_b


def find_missing_eigenvalue(a: np.ndarray, eigenvalues: list[float]) -> float:
    trace_a = np.trace(a)
    missing_eigenvalue = trace_a - sum(eigenvalues)
    return missing_eigenvalue


def answer_full(a: np.array, eps: float) -> None:
    print("Исходная матрица:")
    m = pd.DataFrame(a)
    m.columns = [""] * m.shape[1]
    print(m.to_string(index=False))

    print("\n1. Степенной метод")
    eigenvalue1, eigenvector1, count1 = solve_power_method(a, eps)
    print(f"Максимальное по модулю собственное число: {eigenvalue1}")
    print(f"Собственный вектор: {eigenvector1}")
    print(f"Количество итераций: {count1}")
    print(
        f"Норма вектора невязки в степенном методе: {np.linalg.norm(a @ eigenvector1 -eigenvalue1*eigenvector1, ord = np.inf)}"
    )

    print("\n2. Метод скалярных произведений")
    eigenvalue2, eigenvector2, count2 = solve_dot_product_method(a, eps)
    print(f"Максимальное по модулю собственное число: {eigenvalue2}")
    print(f"Собственный вектор: {eigenvector2}")
    print(f"Количество итераций: {count2}")
    print(
        f"Вектор невязки метода скалярных произведений: {np.linalg.norm(a @ eigenvector2 -eigenvalue2*eigenvector2, ord = np.inf)}"
    )

    print("\n3. Нахождение противоположной границы спектра")
    opposite_eigenvalue, opposite_eigenvector = find_opposite_spectral_bound(a, eps)
    print(f"Противоположное собственное число: {opposite_eigenvalue}")
    print(f"Собственный вектор: {opposite_eigenvector}")
    print(
        f"Норма вектора невязки для противоположной границе спектра: {np.linalg.norm(a @ opposite_eigenvector -opposite_eigenvalue*opposite_eigenvector, ord = np.inf)}"
    )

    print("\n4. Нахождение недостающего собственного числа для матрицы 3x3")
    eigenvalues = [eigenvalue1, opposite_eigenvalue]
    missing_eigenvalue = find_missing_eigenvalue(a, eigenvalues)
    print(f"Недостающее собственное число: {missing_eigenvalue}")


a1 = np.array(
    [
        [-0.907011, -0.277165, 0.445705],
        [-0.277165, 0.633725, 0.077739],
        [0.445705, 0.077739, -0.955354],
    ]
)

e = 1e-10
answer_full(a1, e)
