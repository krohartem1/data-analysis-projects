#include <iostream>
#include <cstdint>
#include <vector>
uint64_t temporary_elevator(uint64_t k, std::vector<uint64_t>& a)
{
	size_t time = 0;
	size_t floor = a.size() - 1;
	int human = 0;
	while (floor != 0)
	{
		if (a[floor] != 0)
		{
			if (a[floor] >= k)
			{
				time += 2*(a[floor] / k) * floor;
				a[floor] = a[floor] % k;
			}
			else
			{
				time +=2*floor;
				human = a[floor];
				a[floor] = 0;
				while (human != 0 && floor !=0)
				{
					if (human + a[floor - 1] < k)
					{
						human += a[floor - 1];
						a[floor - 1] = 0;
						--floor;
					}
					else
					{
						a[floor - 1] -= (k - human);
						human = 0;
					}
				}
			}
		}
		else
		{
			--floor;
		}
	}
	return time;
}
int main()
{
	uint64_t k = 0;
	std::cin >> k;
	size_t n = 0;
	std::cin >> n;
	std::vector<uint64_t> a(n+1);
	a[0] = 0;
	for (size_t i = 1; i <= n; ++i)
	{
		std::cin >> a[i];
	}
std::cout << temporary_elevator(k, a);
	return 0;
}