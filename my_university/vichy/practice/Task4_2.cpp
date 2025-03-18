#include <iostream>
#include <cmath>
#include <vector>
#include <utility>
#include <algorithm>
#include <string>
#include <iomanip>
#include <functional>
using namespace std;

double f(double x, int n)
{
    if (n == -1)
        return cos(5 * x);
    else
        return pow(x, n);
}

double integral_f(double a, double b, int n)
{
    return (pow(b, n + 1) - pow(a, n + 1)) / (n + 1);
}

double integral_g(double a, double b)
{
    return (sin(5 * b) - sin(5 * a)) / 5;
}

double left_rect(double a, double b, int n)
{
    return f(a, n) * (b - a);
}

double right_rect(double a, double b, int n)
{
    return f(b, n) * (b - a);
}

double mid_rect(double a, double b, int n)
{
    return (b - a) * f((a + b) / 2, n);
}

double tr(double a, double b, int n)
{
    return (b - a) * (f(a, n) + f(b, n)) / 2;
}

double Simpson(double a, double b, int n)
{
    return (b - a) * (f(a, n) + f(b, n) + 4 * f((a + b) / 2, n)) / 6;
}

double formula_3_8(double a, double b, int n)
{
    double h = (b - a) / 3;
    return (b - a) * (f(a, n) + 3 * f(a + h, n) + 3 * f(a + 2 * h, n) + f(b, n)) / 8;
}

int main()
{
    double a, b;
    cout << "Введите пределы интегрирования : \n";
    cin >> a >> b;
    cout << "Введите число m - количество разбиений нашего промежутка : \n";
    int m = 0;
    cin >> m;
    cout << "Введите число от 0 до 3, усли хотите выполнить проверку КФ с помощью многочленов соответствующей степени или введите -1, для приближенного вычисления интеграла от функции f(x) = cos(5*x)\n";
    int n = 0;
    cin >> n;
    double result_integr = 0;
    if (n == -1)
        result_integr = integral_g(a, b);
    else
        result_integr = integral_f(a, b, n);
    cout << "Точное значение интеграла : " << result_integr << "\n";
    double h = (b - a) / m;
    cout << "Посчитаем значение интеграла для данной функции на промежутке [a, b] разными способами и сравним с точным значением \n";

    double result_left = 0;
    for (int i = 0; i < m; ++i)
        result_left += left_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ левых прямоугольников : " << result_left << "\n";
    cout << "Погрешность : " << abs(result_integr - result_left) << "\n";
    cout << "Теоретическая погрешность : " << 0.5 * (b - a) * pow(h, 1) * 5 << "\n";

    double result_right = 0;
    for (int i = 0; i < m; ++i)
        result_right += right_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ правых прямоугольников : " << result_right << "\n";
    cout << "Погрешность : " << abs(result_integr - result_right) << "\n";
    cout << "Теоретическая погрешность : " << 0.5 * (b - a) * pow(h, 1) * 5 << "\n";

    double result_mid = 0;
    for (int i = 0; i < m; ++i)
        result_mid += mid_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ средних прямоугольников : " << result_mid << "\n";
    cout << "Погрешность : " << abs(result_integr - result_mid) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 24) * (b - a) * pow(h, 2) * 25 << "\n";

    double result_tr = 0;
    for (int i = 0; i < m; ++i)
        result_tr += tr(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ трапеции : " << result_tr << "\n";
    cout << "Погрешность : " << abs(result_integr - result_tr) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 12) * (b - a) * pow(h, 2) * 25 << "\n";

    double result_simp = 0;
    for (int i = 0; i < m; ++i)
        result_simp += tr(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ Симпсона : " << result_simp << "\n";
    cout << "Погрешность : " << abs(result_integr - result_simp) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 2880) * (b - a) * pow(h, 4) * pow(5, 4) << "\n";

    return 0;
}