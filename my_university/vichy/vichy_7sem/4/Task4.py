import numpy as np
import sympy
import matplotlib.pyplot as plt

a, b = 0, 1
N = 10
h = (b - a) / N
lam = -1


def K_num(x, y):
    return np.cos(x * y) / 2


def K_sym(x, y):
    return sympy.cos(x * y) / 2


f = lambda x: 1 + x - x**2
x_symb, y_symb = sympy.symbols("x y")
f_symb = 1 + x_symb - x_symb**2


def compute_solution(K_expansion, rank):
    alpha_temp = sympy.Poly(K_expansion, y_symb).all_coeffs()
    alpha = [c for c in alpha_temp if c != 0]
    beta_temp = sympy.Poly(K_expansion, x_symb).all_coeffs()
    beta = [c / (c.subs(y_symb, 1)) for c in beta_temp if c != 0]
    # beta = []
    # for c in beta_temp:
    #     if c != 0:
    #         beta.append(c / (c.subs(y_symb, 1)))
    #     else:
    #         beta.append(0)

    alpha_y = [c.subs(x_symb, y_symb) for c in alpha]

    print("Вывод alpha и beta", alpha, "\n", beta)

    gamma = np.zeros((rank, rank))
    for i in range(rank):
        for j in range(rank):
            gamma[i, j] = sympy.integrate(beta[i] * alpha_y[j], (y_symb, a, b))

    B = np.zeros((rank, 1))
    for i in range(rank):
        B[i] = float(sympy.integrate(beta[i] * f(y_symb), (y_symb, a, b)))

    A = np.eye(rank) - lam * gamma
    C = np.linalg.solve(A, B)

    u = f_symb
    for i in range(rank):
        u += lam * float(C[i]) * alpha[i]

    u_values = np.zeros(N + 1)
    for i in range(N + 1):
        x_val = a + i * h
        u_values[i] = float(u.subs(x_symb, x_val))

    return u, u_values


K_3 = (1 / 2) - (1 / 4) * x_symb**2 * y_symb**2 + (1 / 48) * x_symb**4 * y_symb**4
u_3, u_3_values = compute_solution(K_3, 3)

# print(
#     "Вывод разности в точке 0.5, 0.5",
#     K_3.subs(x_symb, 0.5).subs(y_symb, 0.5) - K_num(0.5, 0.5),
# )

K_4 = K_3 - (1 / 1440) * x_symb**6 * y_symb**6
u_4, u_4_values = compute_solution(K_4, 4)

# print(
#     "Вывод разности в точке 0.5, 0.5",
#     K_4.subs(x_symb, 0.5).subs(y_symb, 0.5) - K_num(0.5, 0.5),
# )

# Вывод векторов значений в точках

print("u_3_values", u_3_values)
print("u_4_values", u_4_values)

max_diff = np.max(np.abs(u_4_values - u_3_values))
print("Максимальная разность между u_3 и u_4:", max_diff)

xh = np.linspace(a, b, N + 1)

plt.figure(figsize=(12, 6))
plt.plot(xh, u_3_values, label="u_3(x)", marker="o")
plt.plot(xh, u_4_values, label="u_4(x)", marker="x")
plt.title("Решения u_3(x) и u_4(x)")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(xh, np.abs(u_4_values - u_3_values), label="|u_4(x) - u_3(x)|", marker="o")
plt.title("Разность между u_4(x) and u_3(x)")
plt.xlabel("x")
plt.ylabel("|u_4(x) - u_3(x)|")
plt.legend()
plt.grid()
plt.show()


def compute_gauss(N_nodes):
    leg_poly_expr = sympy.legendre(N_nodes, x_symb)
    leg_poly = sympy.Poly(leg_poly_expr, x_symb)
    T_roots = np.array([float(root) for root in leg_poly.nroots()])
    T_roots = np.sort(T_roots)

    der_legendre_expr = sympy.diff(leg_poly_expr, x_symb)
    der_legendre = sympy.Poly(der_legendre_expr, x_symb)
    A = np.zeros(N_nodes)
    for i in range(N_nodes):
        xi = T_roots[i]
        A[i] = 2 / ((1 - xi**2) * (der_legendre.eval(xi)) ** 2)

    X = 0.5 * (a + b) + 0.5 * (b - a) * T_roots
    A = A * 0.5 * (b - a)

    D = np.eye(N_nodes)
    for j in range(N_nodes):
        for k in range(N_nodes):
            D[j, k] -= lam * A[k] * K_num(X[j], X[k])
    g = np.array([f(X[i]) for i in range(N_nodes)])
    z = np.linalg.solve(D, g)

    # Вывод вектора z
    print("Вектор z:", z)

    u_Gauss = f_symb
    for i in range(N_nodes):
        u_Gauss += lam * A[i] * K_sym(x_symb, X[i]) * z[i]

    u_values = np.zeros(N + 1)
    for i in range(N + 1):
        x_val = a + i * h
        u_values[i] = float(u_Gauss.subs(x_symb, x_val))

    return u_values


u_Gauss_3_values = compute_gauss(3)
u_Gauss_6_values = compute_gauss(6)

# Вывод векторов значений для Гаусса
print("u_Gauss_3_values:", u_Gauss_3_values)
print("u_Gauss_6_values:", u_Gauss_6_values)

plt.figure(figsize=(12, 6))
plt.plot(xh, u_Gauss_3_values, label="u_Gauss_3(x) (3 узла)", marker="o")
plt.plot(xh, u_Gauss_6_values, label="u_Gauss_6(x) (6 узлов)", marker="x")
plt.title("Решение с использование квадратурной формулы Гаусса")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid()
plt.show()

diff_3 = np.abs(u_3_values - u_Gauss_3_values)
diff_4 = np.abs(u_4_values - u_Gauss_6_values)

max_diff_3 = np.max(diff_3)
max_diff_4 = np.max(diff_4)

print(
    f"Максимальная разность (Gauss-3 и Gauss-6): {np.max(np.abs(u_Gauss_6_values - u_Gauss_3_values))}"
)

plt.figure(figsize=(12, 6))
plt.plot(xh, diff_3, label="|u_3(x) - u_Gauss_3(x)|", marker="o")
plt.plot(xh, diff_4, label="|u_4(x) - u_Gauss_6(x)|", marker="x")
plt.title("Сравнение замены ядра и гауссовых квадратурных решений")
plt.xlabel("x")
plt.ylabel("Абсолютная разность")
plt.legend()
plt.grid()
plt.show()
