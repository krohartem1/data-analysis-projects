#include <iostream>
#include <cmath>
#include <cstdint>
//long double scalar_product_alpha(uint64_t xa, uint64_t ya, uint64_t xb, uint64_t yb)
//{
	//return (xa * xb + ya * yb >= 0) ? acos(sqrt(1.0*((xa * xb + ya * yb)*(xa * xb + ya * yb))/ ((xa*xa + ya*ya)*(xb*xb + yb*yb)))) : acos(-sqrt(1.0 * ((xa * xb + ya * yb) * (xa * xb + ya * yb)) / ((xa * xa + ya * ya) * (xb * xb + yb * yb))));
//}

long double Distance(int64_t xa, int64_t ya, int64_t xb, int64_t yb)
{
	long double R_a = sqrt(xa * xa + ya * ya);
	long double R_b = sqrt(xb * xb + yb * yb);
	double alpha = atan2(ya, xa);
	double beta = atan2(yb, xb);
	double gamma = std::abs(alpha - beta);
	if (gamma > 4 * atan2(1, 1))
	{
		gamma = 8 * atan2(1, 1) - gamma;
	}
	if (gamma < 2 && gamma > 0)
	{
		return R_b - R_a + R_a * gamma;
	}
	else if (gamma == 0)
	{
		return R_b - R_a;
	}
	else
	{
		return R_a + R_b;
	}
}

int main()
{
	int64_t xa, ya, xb, yb;
	std::cin >> xa >> ya >> xb >> yb;
	long double R_a = sqrt(xa * xa + ya * ya);
	long double R_b = sqrt(xb * xb + yb * yb);
	if (R_a > R_b)
	{
		int64_t t = xb;
		int64_t c = yb;
		xb = xa;
		yb = ya;
		xa = t;
		ya = c;
	}
	std::cout.precision(7);
	std::cout << Distance(xa, ya, xb, yb);
	return 0;
}