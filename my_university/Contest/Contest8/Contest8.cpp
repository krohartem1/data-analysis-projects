#include <iostream>
#include <vector>
#include<cstdint>
void examination(int n, int a, int b)
{
	uint64_t k = n/a;
	int r = n % a;
	uint64_t length = b - a;
	if (k*length >= r) { std::cout << "Yes" << "\n"; }
	else { std::cout << "No" << "\n"; }
}
int main()
{
	int t;
	std::cin >> t;
	std::vector<std::vector<int>> v(t, std::vector<int>(3));
	for (int i = 0; i < t; ++i)
	{
		std::cin >> v[i][0] >> v[i][1] >> v[i][2];
	}
	for (int i = 0; i < t; ++i)
	{
		examination(v[i][0], v[i][1], v[i][2]);
	}
	return 0;
}