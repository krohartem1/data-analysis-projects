#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
#include <vector>
#include <utility>
#include <algorithm>
#include <string>
#include <iomanip>
using namespace std;

double f(double x, double k)
{
    return pow(M_E, 1.5 * k * x);
}

double f_der(double x, double k)
{
    return 1.5 * k * pow(M_E, 1.5 * k * x);
}

double f_second_der(double x, double k)
{
    return 2.25 * k * k * pow(M_E, 1.5 * k * x);
}

double f_first_num_diff(int i, double k, double h, vector<vector<double>> &table)
{
    return (table[i + 1][1] - table[i - 1][1]) / (2 * h);
}

double f_second_num_diff(int i, double k, double h, vector<vector<double>> &table)
{
    return (table[i + 1][1] - 2 * table[i][1] + table[i - 1][1]) / (h * h);
}

int main()
{
    bool t = 1;
    while (t)
    {
        cout << "Введите m \n";
        int m = 0;
        cin >> m;
        cout << "Введите a и h \n";
        double a, h;
        cin >> a >> h;
        vector<vector<double>> result_table(m + 1, vector<double>(6, 0));
        cout << "Введите коэффициент k \n";
        double k = 0;
        cin >> k;
        for (int i = 0; i < m + 1; ++i)
        {
            result_table[i][0] = a + i * h;
            result_table[i][1] = f(a + i * h, k);
        }

        result_table[0][2] = (-3 * result_table[0][1] + 4 * result_table[1][1] - result_table[2][1]) / (2 * h);
        result_table[m][2] = (3 * result_table[m][1] - 4 * result_table[m - 1][1] + result_table[m - 2][1]) / (2 * h);
        for (int i = 1; i < m; ++i)
        {
            result_table[i][2] = f_first_num_diff(i, k, h, result_table);
        }

        for (int j = 0; j < m + 1; ++j)
        {
            result_table[j][3] = abs(f_der(result_table[j][0], k) - result_table[j][2]);
        }

        result_table[0][4] = (result_table[1][1] - 2 * result_table[0][1] + f(a - h, k)) / (h * h);
        result_table[m][4] = (f(a + (m + 1) * h, k) - 2 * result_table[m][1] + result_table[m - 1][1]) / (h * h);
        for (int i = 1; i < m; ++i)
        {
            result_table[i][4] = f_second_num_diff(i, k, h, result_table);
        }

        for (int j = 0; j < m + 1; ++j)
        {
            result_table[j][5] = abs(f_second_der(result_table[j][0], k) - result_table[j][4]);
        }

        cout << setw(25) << std::left << "x_i" << setw(25) << "f(x_i)" << setw(25) << "f'(x_i)_nd" << setw(25) << "|f'(x_i)-f'(x_i)_nd|" << setw(25) << "f''(x_i)_nd" << setw(25) << "|f''(x_i) - f''(x_i)nd|"
             << "\n";
        for (int i = 0; i < m + 1; ++i)
        {
            for (int j = 0; j < 6; ++j)
            {
                cout << setw(25) << result_table[i][j];
            }
            cout << "\n";
        }

        cout << "Хотите продолжить? \n";
        cout << "(введите Yes или No) \n";
        string s;
        cin >> s;
        if (s == "Yes")
            t = 1;
        else
            t = 0;
    }
    return 0;
}