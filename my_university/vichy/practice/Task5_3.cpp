#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>
#include <algorithm>

// Определим функции f(x) и ρ(x)
double f(double x)
{
    return sin(x);
}

double rho(double x)
{
    return fabs(x - 0.5);
}

// Функция для вычисления узлов и весов методом Гаусса-Лежандра
void gauss_legendre(int n, std::vector<double> &x, std::vector<double> &w)
{
    x.resize(n);
    w.resize(n);

    const double pi = 3.14159265358979323846;
    double z, z1;
    double pp;
    int m = (n + 1) / 2;

    for (int i = 0; i < m; ++i)
    {
        //"Эмпирически полученное начальное приближение"
        z = cos(pi * (i + 0.75) / (n + 0.5));
        do
        {
            // Вычисление функции Лежандра в точке z
            double p1 = 1.0;
            double p2 = 0.0;
            for (int j = 0; j < n; ++j)
            {
                double p3 = p2;
                p2 = p1;
                p1 = ((2.0 * j + 1.0) * z * p2 - j * p3) / (j + 1);
            }
            // Метод Ньютона
            pp = n * (z * p1 - p2) / (z * z - 1.0);
            z1 = z;
            z = z1 - p1 / pp;
        } while (fabs(z - z1) > 1e-10);

        x[i] = -z;
        x[n - 1 - i] = z;
        w[i] = 2.0 / ((1.0 - z * z) * pp * pp);
        w[n - 1 - i] = w[i];
    }
}

// Приближенное вычисление интеграла
double composite_gauss(double a, double b, int N, int m)
{
    double h = (b - a) / m;
    double integral = 0.0;
    std::vector<double> x, w;
    gauss_legendre(N, x, w);
    std::cout << "Roots and weights : \n";
    for (int i = 0; i < m; ++i)
    {
        double a_i = a + i * h;
        double b_i = a + (i + 1) * h;
        double c1 = (b_i + a_i) / 2.0;
        double c2 = (b_i - a_i) / 2.0;

        for (int j = 0; j < N; ++j)
        {
            double t = c1 + c2 * x[j];
            std::cout << t << " " << w[j] << "\n";
            integral += w[j] * rho(t) * f(t) * c2;
        }
    }
    return integral;
}

int main()
{
    double a, b;
    int N, m;

    std::cout << "Введите пределы интегрирования a и b: ";
    std::cin >> a >> b;
    std::cout << "Введите число узлов N и число промежутков деления m: ";
    std::cin >> N >> m;
    std::cout << "Начальные параметры : \n";
    std::cout << "N = " << N << "\n";
    std::cout << "m = " << m << "\n";
    double result = composite_gauss(a, b, N, m);
    std::cout << std::fixed << std::setprecision(12);
    std::cout << "Приближенное значение интеграла: " << result << std::endl;
    std::cout << "Погрешность : " << std::abs(result - 0.112469);
    return 0;
}
