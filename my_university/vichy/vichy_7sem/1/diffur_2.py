import tridiag_matrix as tm
import numpy as np

print("Введите n (n + 1 - порядок системы)")
n = int(input())


def y_solve(x):
    return 1 / (x**2 + 1)


def p_k(x_k):
    return 1.0


def q_k(x_k):
    return -(1 + x_k * x_k)


def r_k(x_k):
    return -2 * x_k


def f_k(x_k):
    return 2 * (3 * x_k**2 - 1) / ((x_k**2 + 1) ** 3)


h = 1 / n
x_vector = np.array([k * h for k in range(0, n + 1)])

a1_diag = np.zeros(n)
c1_diag = np.zeros(n)
a2_diag = np.zeros(n)
c2_diag = np.zeros(n)
b1_diag = np.zeros(n + 1)
b2_diag = np.zeros(n + 1)
d1_diag = np.zeros(n + 1)
d2_diag = np.zeros(n + 1)
for k in range(1, n):
    a1_diag[k - 1] = p_k(x_vector[k]) - (h / 2) * q_k(x_vector[k])
    a2_diag[k - 1] = p_k(x_vector[k]) - (h / 2) * q_k(x_vector[k])
    b1_diag[k] = -2 * p_k(x_vector[k]) + r_k(x_vector[k]) * h**2
    b2_diag[k] = -2 * p_k(x_vector[k]) + r_k(x_vector[k]) * h**2
    c1_diag[k] = p_k(x_vector[k]) + (h / 2) * q_k(x_vector[k])
    c2_diag[k] = p_k(x_vector[k]) + (h / 2) * q_k(x_vector[k])
    d1_diag[k] = f_k(x_vector[k]) * h**2
    d2_diag[k] = f_k(x_vector[k]) * h**2


# 1-й способ(О(h))
def case1(a0, a1, A, b0, b1, B):
    b1_diag[0] = h * a0 + -a1
    c1_diag[0] = a1
    d1_diag[0] = h * A
    a1_diag[n - 1] = -b1
    b1_diag[n] = h * b0 + b1
    d1_diag[n] = h * B
    with open("task1.txt", "w") as inp:
        for x in a1_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in b1_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in c1_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in d1_diag:
            inp.write(str(x) + " ")


# 2-й способ(О(h^2))
def case2(a0, a1, A, b0, b1, B):
    b2_diag[0] = 2 * h * a0 + a1 * (a2_diag[0] / c2_diag[1] - 3)
    c2_diag[0] = a1 * (b2_diag[1] / c2_diag[1] + 4)
    d2_diag[0] = 2 * h * A + a1 * (d2_diag[1] / c2_diag[1])
    a2_diag[n - 1] = -b1 * (4 + b2_diag[n - 1] / a2_diag[n - 2])
    b2_diag[n] = 2 * h * b0 + b1 * (3 - c2_diag[n - 1] / a2_diag[n - 2])
    d2_diag[n] = 2 * h * B - b1 * (d2_diag[n - 1] / a2_diag[n - 2])
    with open("task1.txt", "w") as inp:
        for x in a2_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in b2_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in c2_diag:
            inp.write(str(x) + " ")
        inp.write("\n")
        for x in d2_diag:
            inp.write(str(x) + " ")


# Тут надо написать case1(O(h)) или case2(O(h^2))
# case1(1, -2, 1, 1, 0, 1 / 2)
case2(1, -2, 1, 1, 0, 1 / 2)

y_ans = np.zeros(n + 1)
tm.solve_lin_sys(tm.create_matrix(n), n, y_ans)
print("Максимальная погрешность:", end=" ")
max_mod_ne = 0
for k in range(0, n + 1):
    if max_mod_ne < abs(y_ans[k] - y_solve(x_vector[k])):
        max_mod_ne = abs(y_ans[k] - y_solve(x_vector[k]))
print(max_mod_ne)
