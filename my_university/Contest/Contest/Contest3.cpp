#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <utility>
#include <cmath>
double scalar_product_alpha(int xa, int ya, int xb, int yb)
{
	return acos((xa * xb + ya * yb) / ((sqrt(xa * xa + ya * ya)) * (sqrt(xb * xb + yb * yb))));
}

double Distance(int xa, int ya, int xb, int yb)
{
	double R_a = sqrt(xa * xa + ya * ya);
	double R_b = sqrt(xb * xb + yb * yb);
    if (scalar_product_alpha(xa, ya, xb, yb) < 2)
	{
		return R_b + R_a*(scalar_product_alpha(xa, ya, xb, yb) - 1);
	}
	else
	{
		return R_a + R_b;
	}
}
int main()
{
	int xa, ya, xb, yb;
	std::cin >> xa >> ya >> xb >> yb;
	double R_a = sqrt(xa * xa + ya * ya);
	double R_b = sqrt(xb * xb + yb * yb);
	if (R_a > R_b)
	{
		int t = xb;
		int c = yb;
		xb = xa;
		yb = ya;
		xa = t;
		ya = c;
	}
	std::cout << Distance(xa, ya, xb, yb);
	return 0;
}