import numpy as np
import implementation_of_methods_task3 as iom3

n = 3
epsilon = 1e-5
matrix = np.array(
    [
        [6.9880e-06, -7.1240e-03, 4.37640, 3.99895],
        [6.3880e-03, -0.71240, 1.60640, 1.77052],
        [0.91880, 0.88760, 1.05640, 2.12361],
    ],
    dtype=float,
)
# matrix = np.array(
#     [
#         [6.5176e-06, -8.0648e-03, 4.23528, 3.61628],
#         [5.9176e-03, -0.80648, 1.46528, 1.52097],
#         [0.87176, 0.79352, 0.91528, 1.81150],
#     ]
# )


# Вызов функции
def solve():
    print(
        "Какой метод вы хотите использовать?(1 - Гаусс ед.дел, 2 - Гаусс гл.эл, 3 - LU)"
    )
    print("Введите число: ", end="")
    k = int(input())
    if k == 1:
        iom3.gaussian_elimination_with_determinant(n, matrix, epsilon)
    elif k == 2:
        iom3.gaussian_elimination_with_pivot_and_inverse_check(n, matrix, epsilon)
    elif k == 3:
        iom3.LU_solve_and_print(n, matrix, epsilon)


solve()
