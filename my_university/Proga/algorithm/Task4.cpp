/*#include <algorithm>
#include <iostream>
#include <vector>
#include <cstdint>
#include <cmath>
int main()
{
	size_t n,k;
	std::cin >> n >> k;
	std::vector<int64_t> sort_mass(n);
	std::vector<int64_t> un_sort_mass(k);
	for (size_t i = 0; i < n; ++i)
	{
		std::cin >> sort_mass[i];
	}
	for (size_t i = 0; i < k; ++i)
	{
		std::cin >> un_sort_mass[i];
	}
	auto it = sort_mass.begin();
	auto iter = it;
	for (size_t i = 0; i < k; ++i)
	{
		it = std::lower_bound(sort_mass.begin(), sort_mass.end(), un_sort_mass[i]);
		if (it == sort_mass.end())
		{
			std::cout << *sort_mass.rbegin() << "\n";
		}
		else if (it == sort_mass.begin()) { std::cout << *sort_mass.begin() << "\n"; }
		else
		{
			iter = it;
			int64_t t = *(--iter);
			if (un_sort_mass[i] - t < *it - un_sort_mass[i]) { std::cout << t << "\n"; }
			else if (un_sort_mass[i] - t > *it - un_sort_mass[i]) { std::cout << *it << "\n"; }
			else { std::cout << t << "\n"; }
		}
	}
	return 0;
}*/