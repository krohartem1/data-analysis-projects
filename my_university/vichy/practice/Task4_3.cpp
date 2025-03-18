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

double Runge(int r, double J, double J2)
{
    return (pow(2, r) * J2 - J) / (pow(2, r) - 1);
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
    bool t = 1;
    int i = 0;
    double result_integr = 0;
    if (n == -1)
        result_integr = integral_g(a, b);
    else
        result_integr = integral_f(a, b, n);
    cout << "Точное значение интеграла : " << result_integr << "\n";
    cout << "Посчитаем значение интеграла для данной функции на промежутке [a, b] разными способами и сравним с точным значением \n";

    double h = (b - a) / m;
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
        result_simp += Simpson(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ Симпсона : " << result_simp << "\n";
    cout << "Погрешность : " << abs(result_integr - result_simp) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 2880) * (b - a) * pow(h, 4) * pow(5, 4) << "\n";

    cout << "Введите l - во сколько раз увеличить \n";
    double l = 0;
    cin >> l;
    m *= l;
    ++i;

    cout << "Данные, при измененном m : \n";
    h = (b - a) / m;
    double result_left_h = 0;
    for (int i = 0; i < m; ++i)
        result_left_h += left_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ левых прямоугольников : " << result_left_h << "\n";
    cout << "Погрешность : " << abs(result_integr - result_left_h) << "\n";
    cout << "Теоретическая погрешность : " << 0.5 * (b - a) * pow(h, 1) * 5 << "\n";

    double result_right_h = 0;
    for (int i = 0; i < m; ++i)
        result_right_h += right_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ правых прямоугольников : " << result_right_h << "\n";
    cout << "Погрешность : " << abs(result_integr - result_right_h) << "\n";
    cout << "Теоретическая погрешность : " << 0.5 * (b - a) * pow(h, 1) * 5 << "\n";

    double result_mid_h = 0;
    for (int i = 0; i < m; ++i)
        result_mid_h += mid_rect(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ средних прямоугольников : " << result_mid_h << "\n";
    cout << "Погрешность : " << abs(result_integr - result_mid_h) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 24) * (b - a) * pow(h, 2) * 25 << "\n";

    double result_tr_h = 0;
    for (int i = 0; i < m; ++i)
        result_tr_h += tr(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ трапеции : " << result_tr_h << "\n";
    cout << "Погрешность : " << abs(result_integr - result_tr_h) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 12) * (b - a) * pow(h, 2) * 25 << "\n";

    double result_simp_h = 0;
    for (int i = 0; i < m; ++i)
        result_simp_h += Simpson(a + i * h, a + (i + 1) * h, n);
    cout << "СКФ Симпсона : " << result_simp_h << "\n";
    cout << "Погрешность : " << abs(result_integr - result_simp_h) << "\n";
    cout << "Теоретическая погрешность : " << (1.0 / 2880) * (b - a) * pow(h, 4) * pow(5, 4) << "\n";

    double runge_left = Runge(1, result_left, result_left_h);
    double runge_right = Runge(1, result_right, result_right_h);
    double runge_mid = Runge(2, result_mid, result_mid_h);
    double runge_tr = Runge(2, result_tr, result_tr_h);
    double runge_simp = Runge(4, result_simp, result_simp_h);

    cout << "Значения интегралов уточненных значений: \n";
    cout << "СКФ левого прямоугольника : " << runge_left << " и погрешность " << abs(result_integr - runge_left) << endl;
    cout << "СКФ правого прямоугольника : " << runge_right << " и погрешность " << abs(result_integr - runge_right) << endl;
    cout << "СКФ среднего прямоугольника : " << runge_mid << " и погрешность " << abs(runge_mid - result_integr) << endl;
    cout << "СКФ трапеции : " << runge_tr << " и погрешность " << abs(runge_tr - result_integr) << endl;
    cout << "СКФ Симпсона : " << runge_simp << " и погрешность " << abs(result_integr - runge_simp) << endl;

    return 0;
}