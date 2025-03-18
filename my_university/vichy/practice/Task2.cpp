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
    // return 1 - exp(-2 * x);
}

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

double product_lagrange(double x, int n, int except, vector<pair<double, double>> &table)
{
    double sum = 1;
    for (int j = 0; j < n; ++j)
    {
        if (j != except)
            sum *= (x - table[j].first);
    }
    return sum;
}

double lagrange_interp(double x, int n, vector<pair<double, double>> &table)
{
    double result = 0;
    for (int i = 0; i <= n; ++i)
    {
        result += (product_lagrange(x, n, i, table) / product_lagrange(table[i].first, n, i, table)) * table[i].second;
    }
    return result;
}

int main()
{
    cout << "Задача алгебраического интерполирования"
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
        table[i] = {A + i * h, f(A + i * h)};
    }
    bool t = 1;
    while (t)
    {
        cout << "Введите точку интерполирования : ";
        double x = 0;
        cin >> x;
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
        cout << left << setw(10) << "x_i" << setw(10) << "f(x_i)"
             << "\n";
        for (auto &p : table)
        {
            cout << left << setw(10) << p.first << setw(10) << p.second << "\n";
        }
        cout << "\n";
        sort(table.begin(), table.end(), [x](pair<double, double> p1, pair<double, double> p2)
             { return abs(x - p1.first) < abs(p2.first - x); });
        cout << left << setw(10) << "x_i" << setw(10) << "f(x_i)"
             << "\n";
        for (auto &p : table)
        {
            cout << left << setw(10) << p.first << setw(10) << p.second << "\n";
        }
        cout << "\n";
        cout << "Представление в форме Ньютона дает следующий результат : ";
        double result_newton = newton_interp(x, n, table);
        cout << result_newton << " " << abs(f(x) - result_newton) << "\n";
        cout << "Представление в форме Лагранжа дает следующий результат : ";
        double result_lagrange = lagrange_interp(x, n, table);
        cout << result_lagrange << " " << abs(f(x) - result_lagrange);
        cout << "\n";
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