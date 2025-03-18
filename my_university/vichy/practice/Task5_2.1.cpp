#include <iostream>
#include <cmath>
#include <vector>
#include <algorithm>
const double PI = 3.141592653589793;
// Функция для вычисления значения cos(x^2)
double computeFunction(double x)
{
    return std::cos(x * x);
}

double abs_integral(double a, double b)
{
    return 0.756035277462917;
}
// Функция для вычисления полиномов Лежандра
double legendrePolynomial(int n, double x)
{
    if (n == 0)
        return 1.0;
    if (n == 1)
        return x;
    return (1.0 * (2 * n - 1) * legendrePolynomial(n - 1, x) * x / n) - (1.0 * (n - 1) * legendrePolynomial(n - 2, x) / n);
}
// Функция для нахождения корней полиномов Лежандра методом секущих
std::vector<double> findRoots(double a, double b, int n)
{
    double epsilon = 1e-12;
    int segments = 10000;
    double step = (b - a) / segments;
    std::vector<double> roots;
    std::vector<std::pair<double, double>> z(segments + 1);
    for (int i = 0; i <= segments; ++i)
    {
        double x = a + i * step;
        z[i] = {x, legendrePolynomial(n, x)};
    }

    for (int i = 1; i <= segments; ++i)
    {
        if (z[i - 1].second * z[i].second < 0)
        {
            double x0 = z[i - 1].first;
            double x1 = z[i].first;
            double f0 = z[i - 1].second;
            double f1 = z[i].second;
            double x2;
            do
            {
                x2 = x1 - f1 * (x1 - x0) / (f1 - f0);
                x0 = x1;
                f0 = f1;
                x1 = x2;
                f1 = legendrePolynomial(n, x2);
            } while (std::abs(x1 - x0) >= epsilon);
            roots.push_back(x2);
        }
    }
    if (n % 2 == 1)
        roots.push_back(0);
    std::sort(roots.begin(), roots.end());
    return roots;
}

// Функция для численного интегрирования методом Гаусса
void gaussIntegration()
{
    std::cout << "Gauss formula\n";
    double a = 0;
    double b = PI / 4;
    double c = -1;
    double d = 1;
    std::cout << "Exact value of the integral = " << abs_integral(a, b) << "\n";
    std::cout << "N = 3, 6, 7, 8\n";
    std::cout << "Input N:\n";
    int n;
    std::cin >> n;
    std::vector<double> roots = findRoots(c, d, n);
    std::vector<double> weights(n);

    for (int i = 0; i < roots.size(); ++i)
    {
        double xi = roots[i];
        weights[i] = 2 * (1 - xi * xi) / (n * n * std::pow(legendrePolynomial(n - 1, xi), 2));
    }

    double integral = 0;
    for (int i = 0; i < roots.size(); ++i)
    {
        double xi = roots[i];
        integral += weights[i] * computeFunction(0.5 * (b - a) * xi + 0.5 * (b + a));
    }
    integral *= 0.5 * (b - a);

    std::cout << "Roots and weights:\n";
    for (int i = 0; i < roots.size(); ++i)
    {
        std::cout << roots[i] << " " << weights[i] << "\n";
    }
    std::cout << "Gaussian integral value = " << integral << "\n";
    std::cout << "Eps = " << std::abs(abs_integral(a, b) - integral) << "\n";
}

int main()
{
    while (true)
    {
        gaussIntegration();
        std::cout << "Do you want to continue? [1 - Yes, 0 - No]\n";
        int p = 0;
        std::cin >> p;
        if (p)
            continue;
        else
            break;
    }
    return 0;
}
