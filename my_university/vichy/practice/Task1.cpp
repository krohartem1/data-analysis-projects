#include <iostream>
#include <cmath>
#include <vector>
#include <utility>
#include <tuple>
using namespace std;

double f(double x)
{
    return x - 10 * sin(x);
}

double der_f(double x)
{
    return 1 - 10 * cos(x);
}

double second_der_f(double x)
{
    return 10 * sin(x);
}

int root_separation(vector<pair<double, double>> &intervals, int N, double A, double B)
{
    double H = (B - A) / N;
    int count = 0;
    for (double x1 = A; x1 <= B - H; x1 += H)
    {
        if (f(x1) * f(x1 + H) <= 0)
        {
            ++count;
            intervals.push_back({x1, x1 + H});
        }
    }
    return count;
}

tuple<double, double, double, int> bisection(double a, double b, double eps)
{
    int count = 0;
    while (b - a > 2 * eps)
    {
        ++count;
        if (f(a) * f((a + b) / 2) < 0)
        {
            b = (a + b) / 2;
        }
        else
            a = (a + b) / 2;
    }
    return {(a + b) / 2, (b - a), abs(f((a + b) / 2)), count};
}

pair<double, int> newton_method(double a, double b, double eps)
{
    double x0 = (a + b) / 2;
    int count = 0;
    double x1 = x0 - (f(x0) / der_f(x0));
    while (abs(x1 - x0) > eps)
    {
        ++count;
        x0 = x1;
        x1 = x0 - (f(x0) / der_f(x0));
    }
    return {x1, count};
}

pair<double, int> modify_newton_method(double a, double b, double eps)
{
    int count = 0;
    double x0 = (a + b) / 2;
    double x_begin = x0;
    double x1 = x0 - (f(x0) / der_f(x0));
    while (abs(x1 - x0) > eps)
    {
        ++count;
        x0 = x1;
        x1 = x0 - (f(x0) / der_f(x_begin));
    }
    return {x1, count};
}

pair<double, int> secant_method(double a, double b, double eps)
{
    int count = 0;
    double x0 = (a + b) / 2;
    double x1 = x0 - (f(x0) / der_f(x0));
    double x2 = x1 - (f(x1) / (f(x1) - f(x0))) * (x1 - x0);
    while (abs(x2 - x1) > eps)
    {
        ++count;
        x0 = x1;
        x1 = x2;
        x2 = x1 - (f(x1) / (f(x1) - f(x0))) * (x1 - x0);
    }
    return {x2, count};
}

int main()
{
    int A = -5;
    int B = 3;
    double eps = 0.000001;
    cout << "Численные методы решения нелинейных уравнений \n";
    cout << "Параметры задачи : \n";
    cout << "A = -5, B = 3, eps = 0.000001 \n";
    cout << "f(x) = x - 10*sin(x) \n";
    int N = 0;
    cout << "Введите N : \n";
    cin >> N;
    vector<pair<double, double>> intervals;
    int count = root_separation(intervals, N, A, B);
    for (auto &x : intervals)
    {
        cout << x.first << " " << x.second << "\n";
    }
    cout << "Количество отрезков : " << count << "\n";
    cout << "\n";
    cout << "Метод бисекций"
         << " \n";
    for (auto &x : intervals)
    {
        cout << "Начальное приближение к корню : " << (x.first + x.second) / 2 << "\n";
        tuple<double, double, double, int> ans = bisection(x.first, x.second, eps);
        cout << "Количество шагов (m) : " << get<3>(ans) << "\n";
        cout << "Приближенное решение : " << get<0>(ans) << "\n";
        cout << get<1>(ans) << "\n";
        cout << get<2>(ans) << "\n";
        cout << "\n";
    }

    cout << "Метод Ньютона"
         << " \n";
    for (auto &x : intervals)
    {
        cout << "Начальное приближение к корню : " << (x.first + x.second) / 2 << "\n";
        pair<double, int> ans = newton_method(x.first, x.second, eps);
        cout << "Количество шагов (m) : " << ans.second << "\n";
        cout << "Приближенное решение : " << ans.first << "\n";
        cout << abs(f(ans.first) - 0) << "\n";
        cout << "\n";
    }
    cout << "Модифицированный метод Ньютона \n";
    for (auto &x : intervals)
    {
        cout << "Начальное приближение к корню : " << (x.first + x.second) / 2 << "\n";
        pair<double, int> ans = modify_newton_method(x.first, x.second, eps);
        cout << "Количество шагов (m) : " << ans.second << "\n";
        cout << "Приближенное решение : " << ans.first << "\n";
        cout << abs(f(ans.first) - 0) << "\n";
        cout << "\n";
    }
    cout << "Метод секущих \n";
    for (auto &x : intervals)
    {
        cout << "Начальное приближение к корню : " << (x.first + x.second) / 2 << "\n";
        pair<double, int> ans = secant_method(x.first, x.second, eps);
        cout << "Количество шагов (m) : " << ans.second << "\n";
        cout << "Приближенное решение : " << ans.first << "\n";
        cout << abs(f(ans.first) - 0) << "\n";
        cout << "\n";
    }
    return 0;
}