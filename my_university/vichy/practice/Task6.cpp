#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

using namespace std;

double computeTerm(int order, double x)
{
    double result;
    switch (order)
    {
    case 0:
        result = exp(-0.5 * pow(x, 2) - x);
        break;
    case 1:
        result = -computeTerm(0, x) * (1 + x);
        break;
    case 2:
        result = -computeTerm(1, x) - computeTerm(1, x) * x - computeTerm(0, x);
        break;
    case 3:
        result = -computeTerm(2, x) - computeTerm(2, x) * x - 2 * computeTerm(1, x);
        break;
    case 4:
        result = -computeTerm(3, x) - computeTerm(3, x) * x - 3 * computeTerm(2, x);
        break;
    default:
        result = 0;
        break;
    }
    return result;
}

double func(double x, double y)
{
    return -y * (1 + x);
}

double factorial(int n)
{
    if (n == 0)
    {
        return 1;
    }
    return n * factorial(n - 1);
}

double taylorSeries(double (*termFunc)(int, double), double x0, double x)
{
    double sum = 0;
    for (int i = 0; i < 4; ++i)
    {
        double term = termFunc(i, x0) / factorial(i);
        for (int k = 1; k <= i; ++k)
        {
            term *= (x - x0);
        }
        sum += term;
    }
    return sum;
}

double adamsMethod(vector<vector<double>> &diffTable, vector<vector<double>> &approxTable, int step, double h)
{
    double ym = approxTable[step - 1][1] + diffTable[step - 1][0] + 0.5 * diffTable[step - 2][1] +
                5 * diffTable[step - 3][2] / 12 + 3 * diffTable[step - 4][3] / 8 + 251 * diffTable[step - 5][4] / 720;
    diffTable[step][0] = (-ym * (1 + approxTable[step][0])) * h;
    diffTable[step - 1][1] = diffTable[step][0] - diffTable[step - 1][0];
    diffTable[step - 2][2] = diffTable[step - 1][1] - diffTable[step - 2][1];
    diffTable[step - 3][3] = diffTable[step - 2][2] - diffTable[step - 3][2];
    diffTable[step - 4][4] = diffTable[step - 3][3] - diffTable[step - 4][3];
    return ym;
}

double rungeKutta(double xn, double yn, double h)
{
    double k1 = h * func(xn, yn);
    double k2 = h * func(xn + h / 2, yn + k1 / 2);
    double k3 = h * func(xn + h / 2, yn + k2 / 2);
    double k4 = h * func(xn + h, yn + k3);
    return yn + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
}

double eulerMethod(double xn, double yn, double h)
{
    return yn + h * func(xn, yn);
}

double Euler1(double xk, double yk, double h)
{
    double temp = eulerMethod(xk, yk, h / 2);
    return yk + h * func(xk + h / 2, temp);
}

double Euler2(double xk, double yk, double h)
{
    double temp = eulerMethod(xk, yk, h / 2);
    return yk + h * (func(xk, yk) + func(xk + h, temp)) / 2;
}

void printTable(const vector<vector<double>> &table, int columns)
{
    for (const auto &row : table)
    {
        for (int j = 0; j < columns; ++j)
        {
            cout << setw(25) << std::left << row[j];
        }
        cout << "\n";
    }
    cout << "\n\n";
}

int main()
{
    double x0 = 0;
    double y0 = 1;
    double h = 0.1;
    int N = 10;
    cout << "Таблица истинных значений : \n";
    vector<vector<double>> values(N + 3, vector<double>(2));
    for (int k = -2; k <= 10; ++k)
    {
        values[k + 2][0] = x0 + k * h;
        values[k + 2][1] = computeTerm(0, values[k + 2][0]);
    }
    cout << setw(25) << std::left << "x" << setw(25) << "f(x)\n";
    printTable(values, 2);
    cout << "Таблица значений по Тейлору : \n";
    vector<vector<double>> taylorValues(N + 3, vector<double>(3));
    for (int k = -2; k <= 10; ++k)
    {
        taylorValues[k + 2][0] = x0 + k * h;
        taylorValues[k + 2][1] = taylorSeries(computeTerm, x0, values[k + 2][0]);
        taylorValues[k + 2][2] = abs(values[k + 2][1] - taylorValues[k + 2][1]);
    }
    cout << setw(25) << std::left << "x" << setw(25) << "f_T(x)" << setw(25) << "|f_T(x) - f(x)|\n";
    printTable(taylorValues, 3);
    cout << "Таблица значений по Адамсу : \n";
    vector<vector<double>> adamsValues(N + 3, vector<double>(3));
    for (int k = -2; k <= 2; ++k)
    {
        adamsValues[k + 2][0] = taylorValues[k + 2][0];
        adamsValues[k + 2][1] = taylorValues[k + 2][1];
    }

    vector<vector<double>> diffTable(N + 3, vector<double>(5));
    for (int i = 0; i <= 4; ++i)
    {
        diffTable[i][0] = h * computeTerm(1, taylorValues[i][0]);
    }
    for (int i = 1; i <= 4; ++i)
    {
        for (int k = 0; k <= 4 - i; ++k)
        {
            diffTable[k][i] = diffTable[k + 1][i - 1] - diffTable[k][i - 1];
        }
    }

    for (int i = 5; i < N + 3; ++i)
    {
        adamsValues[i][0] = taylorValues[i][0];
        adamsValues[i][1] = adamsMethod(diffTable, adamsValues, i, h);
        adamsValues[i][2] = abs(values[i][1] - adamsValues[i][1]);
    }
    cout << setw(25) << std::left << "x" << setw(25) << "f_A(x)" << setw(25) << "|f_A(x) - f(x)|\n";
    printTable(adamsValues, 3);
    cout << "Таблица по методу Рунге-Кутты : \n";
    vector<vector<double>> rungeKuttaValues(N + 1, vector<double>(3));
    rungeKuttaValues[0][0] = x0;
    rungeKuttaValues[0][1] = y0;
    for (int i = 1; i <= N; ++i)
    {
        rungeKuttaValues[i][0] = x0 + h * i;
        rungeKuttaValues[i][1] = rungeKutta(rungeKuttaValues[i - 1][0], rungeKuttaValues[i - 1][1], h);
        rungeKuttaValues[i][2] = abs(rungeKuttaValues[i][1] - values[i + 2][1]);
    }
    cout << setw(25) << std::left << "x" << setw(25) << "f_R_K(x)" << setw(25) << "|f_R_K(x) - f(x)|\n";
    printTable(rungeKuttaValues, 3);
    cout << "Таблица по Эйлеру : \n";
    vector<vector<double>> eulerValues(N + 1, vector<double>(7));
    eulerValues[0][0] = x0;
    eulerValues[0][1] = y0;
    for (int i = 1; i <= N; ++i)
    {
        eulerValues[i][0] = eulerValues[i - 1][0] + h;
        eulerValues[i][1] = eulerMethod(eulerValues[i - 1][0], eulerValues[i - 1][1], h);
        eulerValues[i][2] = abs(eulerValues[i][1] - values[i + 2][1]);
        eulerValues[i][3] = Euler1(eulerValues[i - 1][0], eulerValues[i - 1][1], h);
        eulerValues[i][4] = abs(eulerValues[i][3] - values[i + 2][1]);
        eulerValues[i][5] = Euler2(eulerValues[i - 1][0], eulerValues[i - 1][1], h);
        eulerValues[i][6] = abs(eulerValues[i][5] - values[i + 2][1]);
    }
    cout << setw(20) << std::left << "x" << setw(20) << "f_E(x)" << setw(20) << "|f_E(x) - f(x)|" << setw(20) << "f_E1(x)" << setw(20) << "|f_E1(x) - f(x)|" << setw(20) << "f_E2(x)" << setw(20) << "|f_E2(x) - f(x)|\n";
    printTable(eulerValues, 7);

    return 0;
}
