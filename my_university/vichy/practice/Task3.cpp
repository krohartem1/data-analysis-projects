#include <iostream>
#include <iomanip>
#include <cmath>
#include <vector>
#include <utility>
#include <algorithm>
#include <string>
using namespace std;

double f(double x)
{
    return 2 * sin(x) - x / 2;
}
// first solve
double product(double x, int i, vector<pair<double, double>> &table)
{
    double sum = 1;
    for (int j = 0; j < i; ++j)
    {
        sum *= (x - table[j].first);
    }
    return sum;
}

double newton_interp(double x, int n, vector<pair<double, double>> &table)
{
    if (table[0].first == x)
        return table[0].second;
    vector<double> coef(n + 1, 0);
    coef[0] = table[0].second;
    for (int i = 1; i <= n; ++i)
    {
        double sum = coef[0];
        for (int j = 1; j != i; ++j)
        {
            sum += coef[j] * product(table[i].first, j, table);
        }
        coef[i] = (table[i].second - sum) / product(table[i].first, i, table);
    }

    double result = coef[0];
    for (int j = 1; j <= n; ++j)
    {
        result += coef[j] * product(x, j, table);
    }
    return result;
}

// second solve

double product_2(double x, int i, vector<pair<double, double>> &table)
{
    double sum = 1;
    for (int j = 0; j < i; ++j)
    {
        sum *= (x - table[j].second);
    }
    return sum;
}

vector<double> newton_interp_2(int n, vector<pair<double, double>> &table)
{
    vector<double> coef(n + 1, 0);
    coef[0] = table[0].first;
    // if (table[0].first == x)
    //  return coef;
    for (int i = 1; i <= n; ++i)
    {
        double sum = coef[0];
        for (int j = 1; j != i; ++j)
        {
            sum += coef[j] * product_2(table[i].second, j, table);
        }
        coef[i] = (table[i].first - sum) / product_2(table[i].second, i, table);
    }
    return coef;
}

double f_2(double x, int n, double F, vector<pair<double, double>> &table, vector<double> &coef)
{
    double result = coef[0];
    for (int j = 1; j <= n; ++j)
    {
        result += coef[j] * product_2(x, j, table);
    }
    return result - F;
}

int root_separation(vector<pair<double, double>> &intervals, int N, int n, vector<pair<double, double>> &table, vector<double> &coef, double F, double A, double B)
{
    double H = (B - A) / N;
    int count = 0;
    for (double x1 = A; x1 <= B - H; x1 += H)
    {
        if (f_2(x1, n, F, table, coef) * f_2(x1 + H, n, F, table, coef) <= 0)
        {
            ++count;
            intervals.push_back({x1, x1 + H});
        }
    }
    return count;
}

double bisection(double a, double b, double eps, int n, double F, vector<pair<double, double>> &table, vector<double> &coef)
{
    while (b - a > 2 * eps)
    {
        if (f_2(a, n, F, table, coef) * f_2((a + b) / 2, n, F, table, coef) < 0)
        {
            b = (a + b) / 2;
        }
        else
            a = (a + b) / 2;
    }
    return (a + b) / 2;
}
//

int main()
{
    double eps = 1.0E-8;
    cout << "Задача обратного интерполирования"
         << "\n"
         << "Вариант 8"
         << "\n";
    int m = 0;
    cout << "Введите число значений в таблице : ";
    cin >> m;
    cout << "\n";
    cout << "Введите границы интервала : ";
    double A, B;
    cin >> A >> B;
    cout << "\n";
    vector<pair<double, double>> table(m + 1);
    double h = (B - A) / m;
    for (int i = 0; i <= m; ++i)
    {
        table[i] = {f(A + i * h), A + i * h};
    }
    bool t = 1;
    while (t)
    {
        cout << "Введите точку интерполирования : ";
        double F = 0;
        cin >> F;
        cout << "\n";

        cout << "Введите степень интерполяционного многочлена : ";
        int n = 0;
        cin >> n;
        while (n > m)
        {
            cout << "Введено недопустимое значение n, введите заново"
                 << "\n";
            cin >> n;
        }
        sort(table.begin(), table.end(), [F](pair<double, double> p1, pair<double, double> p2)
             { return abs(F - p1.first) < abs(p2.first - F); });
        cout << left << setw(10) << "f(x_i)" << setw(10) << "x_i"
             << "\n";
        for (auto &p : table)
        {
            cout << left << setw(10) << p.first << setw(10) << p.second << "\n";
        }
        cout << "\n";
        cout << "Первый способ : ";
        double result_newton = newton_interp(F, n, table);
        cout << result_newton << " " << abs(f(result_newton) - F) << "\n";
        vector<pair<double, double>> intervals;
        int N = 100000;
        vector<double> coef = newton_interp_2(n, table);
        root_separation(intervals, N, n, table, coef, F, A, B);
        cout << "Второй способ : ";
        for (auto &t : intervals)
        {
            double result_bisection = bisection(t.first, t.second, eps, n, F, table, coef);
            cout << result_bisection << " " << abs(f(result_bisection) - F) << "\n";
        }
        cout << "Хотите продолжить? \n";
        string s;
        cin >> s;
        if (s == "Yes")
            t = 1;
        else
            t = 0;
    }
    return 0;
}