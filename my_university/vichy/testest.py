import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse as sp
from scipy.sparse import linalg
import time
import math

a = 0
b = 1


# Вариант 1
def p(x):
    return 1


def r(x):
    return 2 * x


def f(x):
    return (2 * (3 * x * x - 1)) / ((x * x + 1) ** 3)


def q(x):
    return 0


def progonka(K, F, N):
    start_time = time.time()
    s = np.zeros(N - 2)
    t = np.zeros(N - 1)
    y = sp.lil_matrix((N - 1, 1))
    s[0] = -K[0, 1] / K[0, 0]
    t[0] = F[0, 0] / K[0, 0]
    for i in range(1, N - 2):
        s[i] = -K[i, i + 1] / (K[i, i] + K[i, i - 1] * s[i - 1])
    for i in range(1, N - 1):
        t[i] = (F[i, 0] - K[i, i - 1] * t[i - 1]) / (K[i, i] + K[i, i - 1] * s[i - 1])
        y[N - 2, 0] = t[N - 2]
    for i in range(N - 3, -1, -1):
        y[i, 0] = s[i] * y[i + 1, 0] + t[i]
        work_time = time.time() - start_time
    return y, work_time


def Jacoby(K, G, err, maxNum, N, sigma):
    start_time = time.time()
    u_new = sp.lil_matrix((N - 1, 1))
    D = sp.lil_matrix((N - 1, N - 1))
    D.setdiag(K.diagonal())
    D = D.power(-1)
    u_old = sp.lil_matrix((N - 1, 1))
    for i in range(maxNum):
        u_old = u_new
        u_new = u_old - sigma * D.dot((K.dot(u_old) - G))
        u_new_t = u_new
        u_old_t = u_old
        if np.linalg.norm(u_new_t.toarray() - u_old_t.toarray()) < err:
            break
    work_time = time.time() - start_time
    return u_new, work_time


def coef(p, r, f, N):
    h = 1 / N
    B = np.zeros(N - 1)
    A = np.zeros(N - 2)
    K = sp.lil_matrix((N - 1, N - 1))
    F = sp.lil_matrix((N - 1, 1))

    for i in range(N - 1):
        F[i, 0] = integ_phi_i(f, i * h, h)

    for i in range(N - 1):
        B[i] = integ_phi_ii(r, i * h, h) + integ_der_ii(p, i * h, h)

    for i in range(N - 2):
        A[i] = integ_phi_ij(r, i * h, h) + integ_der_ij(p, i * h, h)

    # заполним матрицу K
    for i in range(N - 1):
        K[i, i] = B[i]
    for i in range(N - 2):
        K[i, i + 1] = A[i]
    for i in range(N - 2):
        K[i + 1, i] = A[i]

    return K, F


# функции интегрирования базисных функций
# (подынтегральную фунцию приблизим значением в средней точке и проинтегрируем только


# для одной базисной фунции (площадь треугольника)
def integ_phi_i(f, x, h):
    return f(x + h) * h


# для совпадающих функций i = j (проинтегрировали произведение базисных функций


def integ_phi_ii(f, x, h):
    return (2 / 3) * f(x + h) * h


# для сдвинутых j = i + 1
def integ_phi_ij(f, x, h):
    return (1 / 6) * f(x + (1.5 * h)) * h


# для совпадающих производных (разбили на 2 треугольник)
def integ_der_ii(f, x, h):
    return (f(x + (0.5 * h)) + f(x + (1.5 * h))) / h


# со сдвигом
def integ_der_ij(f, x, h):
    return -f(x + (1.5 * h)) / h


def define_sigma(K, N):
    h = 1 / N
    sum_of_elem = np.zeros(N - 1)

    sum_of_elem[0] = K[0, 0] + K[1, 0]
    for j in range(1, N - 2):
        sum_of_elem[j] = K[j, j] + K[j - 1, j] + K[j + 1, j]

    sum_of_elem[N - 2] = K[N - 2, N - 2] + K[N - 3, N - 2]

    return 2 / np.max(sum_of_elem)


def Transformation_matrix(N):
    n = int(math.sqrt(N))
    C = sp.lil_matrix((N - 1, N - 1))
    for i in range(N - 1):
        C[i, i] = 1

    kn = 1
    for i in range(0, (n - 1) * (n - 1)):
        C[i, n * (n - 1) + i // (n - 1)] = kn / n
        # C[n*(n-1)+i//(n-1), i] = kn/n
        kn += 1
        if kn == n:
            kn = 1
    kn = n - 1
    for i in range(n - 1, (n - 1) * n):
        C[i, n * (n - 1) + i // (n - 1) - 1] = kn / n
        # C[n*(n-1)+i//(n-1)-1, i] = kn/n
        kn -= 1
        if kn == 0:
            kn = n - 1

    return C


def decomp(K, F, err, maxNum, N, sigma):
    start_time = time.time()
    n = int(math.sqrt(N))
    h = 1 / N

    # формируем предобуславливатель
    Delta_Hh = sp.lil_matrix((N - 1, N - 1))
    Delta = sp.lil_matrix((N - 1, N - 1))

    for i in range(0, n * (n - 1)):
        Delta[i, i] = 2

    # for i in range (0, n*(n-1), n-2):
    #     Delta[i,i] = 1

    for i in range(0, n * (n - 1) - 2):
        Delta[i, i + 1] = -1
        Delta[i + 1, i] = -1

    Delta = Delta * 1 / h

    for i in range(n * (n - 1), n * n - 1):
        Delta_Hh[i, i] = 2

    # for i in range (n*(n-1), n*n-1, n-2):
    #     Delta[i,i] = 1

    for i in range(n * (n - 1), n * n - 2):
        Delta_Hh[i, i + 1] = -1
        Delta_Hh[i + 1, i] = -1

    Delta_Hh = Delta_Hh / (h * n)
    Delta_Hh += Delta

    p_arr = np.zeros(101)
    h1 = 1 / 100
    for i in range(101):
        p_arr[i] = p(i * h1)

    p_mean = np.mean(p_arr)
    Delta_Hh = Delta_Hh * p_mean

    # матрица преобразования
    C = Transformation_matrix(N)
    KDD = sp.lil_matrix((N - 1, N - 1))
    CT = C
    CT.transpose()
    KDD = CT.dot(K.dot(C))

    FDD = sp.lil_matrix((N - 1, 1))
    FDD = CT.dot(F)

    u_new = sp.lil_matrix((N - 1, 1))
    u_old = sp.lil_matrix((N - 1, 1))
    counter = 0
    for i in range(maxNum):
        u_old = u_new
        counter += 1
        d_k = KDD.dot(u_old) - FDD  # 1

        w_k, _ = progonka(Delta_Hh, sigma * d_k, N)

        u_new = u_old - w_k

        if np.linalg.norm(u_new.toarray() - u_old.toarray()) < err:
            break

    u_new = C.dot(u_new)
    work_time = time.time() - start_time
    return u_new, work_time, counter


# Вызов функций
# N - количество элементов в сетке для метода прогонки и Якоби
N = 100
h = 1 / N
K, F = coef(p, r, f, N)
sigma = define_sigma(K, N)
y, work_time = progonka(K, F, N)
yJ, work_timeJ = Jacoby(K, F, 10**-4, 10000, N, sigma)
xh = np.arange(h, 1, h)
# N1 - количество элементов в сетке для метода декомпозиции
N1 = 100
h1 = 1 / N1
K1, F1 = coef(p, r, f, N1)
yD, work_timeD, counter = decomp(K1, F1, 10**-4, 10000, N1, sigma)
xhD = np.arange(h1, 1, h1)
# вывод таблицы значений
print("N = ", N, ":")
print("Времена выполнения:")
print(
    "Прогонка: ",
    work_time,
    " Якоби: ",
    work_timeJ,
    " Декомпозиция: ",
    work_timeD,
    "сек\n",
)
print("x".center(3), "U1(x)".center(15), "U2(x)".center(15), "U3(x)".center(15))
for i in range(1, 10):
    print(
        "%2.1f %15.12f %15.12f %15.12f "
        % (i * 0.1, y[(N * i) // 10, 0], yJ[(N * i) // 10, 0], yD[(N1 * i) // 10, 0])
    )
    print("\n")
    print("№".center(7), "A".center(15), "B".center(17), "C".center(17), "F".center(17))
for i in range(1, 10):
    print(
        "%4d %16.12f %16.12f %16.12f "
        % (
            (N * i) // 10,
            K[(N * i) // 10, (N * i) // 10],
            K[(N * i) // 10, ((N * i) // 10) - 1],
            K[(N * i) // 10, ((N * i) // 10) + 1],
        ),
        F[(N * i) // 10, 0],
    )
# Строим графики
plt.figure(figsize=(12, 7))
plt.subplot(1, 3, 1)
plt.grid(True)
# plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
plt.title("Прогонка N=" + str(N), fontsize=9)
plt.xlabel("x", fontsize=15, color="gray")
plt.ylabel("y(x)", fontsize=15, color="gray")
plt.plot(xh, y.toarray())
plt.subplot(1, 3, 2)
plt.grid(True)
plt.title("Якоби N=" + str(N), fontsize=9)
plt.xlabel("x", fontsize=15, color="gray")
plt.plot(xh, yJ.toarray())
plt.subplot(1, 3, 3)
plt.grid(True)
plt.title("Декомпозиция N=" + str(N1), fontsize=9)
plt.xlabel("x", fontsize=15, color="gray")
plt.plot(xhD, yD.toarray())
plt.show()
