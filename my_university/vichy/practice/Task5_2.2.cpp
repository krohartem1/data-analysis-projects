#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>
const double PI = 3.141592653589793;
double calculateFunction(double x)
{
    return std::exp(x) * std::sin(x * x);
}

void calculateMehlerIntegral()
{
    std::cout << "Enter  N1, N2, and N3:\n";
    std::vector<int> n(3);
    for (int i = 0; i < 3; ++i)
    {
        std::cin >> n[i];
    }

    for (int numPoints : n)
    {
        double integralSum = 0.0;
        std::cout << "Roots : \n";
        for (int k = 0; k < numPoints; ++k)
        {
            double x = std::cos((2 * k + 1) * PI / (2 * numPoints));
            std::cout << x << "\n";
            integralSum += calculateFunction(x);
        }
        integralSum *= PI / numPoints;
        std::cout << "Calculated integral using Mehler quadrature = " << std::setprecision(12) << integralSum << '\n';
    }
}

int main()
{
    std::cout << "Integral calculation using Mehler quadrature formula\n";
    std::cout << "a = -1, b = 1\n";
    calculateMehlerIntegral();
    return 0;
}
