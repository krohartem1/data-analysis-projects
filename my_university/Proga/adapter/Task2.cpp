/*#include <iostream>
#include <vector>
#include <set>
int main()
{
	int n, k;
	std::cin >> n >> k;
	int x = 0;
	std::vector<int> v(n);
	std::multiset<int> multi;
	for(int i = 0; i <= n; ++i)
	{
		if (i == n)
		{
			std::cout << *multi.begin();
		}
		else
		{
			std::cin >> v[i];
			if (i >= k)
			{
				std::cout << *multi.begin() << "\n";
				multi.erase(multi.lower_bound(v[i-k]));
				multi.insert(v[i]);
			}
			else { multi.insert(v[i]); }
		}
	}
	return 0;
}*/