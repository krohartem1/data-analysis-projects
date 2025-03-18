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
    cout << "Введите число от 0 до 3, усли хотите выполнить проверку КФ с помощью многочленов соответствующей степени или введите -1, для приближенного вычисления интеграла от функции f(x) = cos(5*x)\n";
    int n = 0;
    cin >> n;
    double result_integr = 0;
    if (n == -1)
        result_integr = integral_g(a, b);
    else
        result_integr = integral_f(a, b, n);
    cout << "Точное значение интеграла : " << result_integr << "\n";

    cout << "Посчитаем значение интеграла для данной функции на промежутке [a, b] разными способами и сравним с точным значением \n";
    cout << "КФ левых прямоугольников : " << abs(result_integr - left_rect(a, b, n)) << "\n";
    cout << "КФ правых прямоугольников : " << abs(result_integr - right_rect(a, b, n)) << "\n";
    cout << "КФ средних прямоугольников : " << abs(result_integr - mid_rect(a, b, n)) << "\n";
    cout << "КФ трапеции : " << abs(result_integr - tr(a, b, n)) << "\n";
    cout << "КФ Симпсона : " << abs(result_integr - Simpson(a, b, n)) << "\n";
    cout << "КФ 3/8 : " << abs(result_integr - formula_3_8(a, b, n)) << "\n";
    return 0;
}