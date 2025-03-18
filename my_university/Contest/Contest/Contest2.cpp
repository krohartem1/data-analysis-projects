#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <utility>
#include <numeric>
std::pair<uint16_t, uint16_t> Sum(std::pair<uint16_t, uint16_t> num, std::pair<uint16_t, uint16_t> denum)
{
	uint16_t M_0 = num.first*denum.second + num.second * denum.first;
	uint16_t N_0 = num.second * denum.second;
	uint16_t p = gcd(M_0, N_0);
	std::pair<uint16_t, uint16_t> MN;
	MN.first = M_0 / p;
	MN.second = N_0 / p;
	return MN;
}
int main()
{
	uint16_t a, b, c, d;
	std::cin >> a >> b >> c >> d;
	std::pair<uint16_t, uint16_t> ab = { a,b };
	std::pair<uint16_t, uint16_t> cd = { c,d };
	std::cout << Sum(ab, cd).first << " " << Sum(ab, cd).second;
	return 0;
}