#include <iostream>
#include <cstdint>
#include <vector>
int main()
{
	size_t n = 0;
	std::cin >> n;
	std::vector<uint32_t>a(n);
	for (size_t i = 0; i < n; ++i) { std::cin >> a[i];}
	int Sum1 = 0;
	for (size_t j = 0; j < n; ++j)
	{
		 Sum1 = Sum1 + a[j] - a[0];
	}
	std::cout << Sum1 << " ";
	int Sum = Sum1;
	for (size_t i = 1; i < n ; ++i) {
		Sum = Sum + (2 * i - n) * (a[i] - a[i - 1]);
		std::cout << Sum << " "; 
	}
	return 0;
}