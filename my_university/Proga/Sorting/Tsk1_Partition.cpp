/*#include <iostream>
#include <vector>
#include <string>
std::vector<int>::iterator partition(std::vector<int>& mass, int x)
{
	if (mass.empty()) { return mass.end(); }
	auto G = mass.begin();
	auto P = mass.begin();
	if (*mass.begin() < x)
	{
		P = std::next(mass.begin());
		G = std::next(mass.begin());
	}
	else if (*mass.begin() == x)
	{
		G = std::next(mass.begin());
	}
	for (auto it = ++mass.begin(); it != mass.end(); ++it)
	{
		if (*it < x)
		{
			int y = *it;
			*it = *G;
			*G = *P;
			*P = y;
			++G;
			++P;
		}
		else if (*it == x)
		{
			*it = *G;
			*G = x;
			++G;
		}
	}
	return P;
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::string s;
	std::vector<int> mass(N);
	for (int i = 0; i < N; ++i)
	{
		std::cin >> mass[i];
	}
	int x = 0;
	std::cin >> x;
	auto iter = partition(mass, x);
	int sum = 0;
	if (mass.empty()) { sum = 0; }
	else {
		for (auto it = mass.begin(); it != iter; ++it)
		{
			++sum;
		}
	}
	
	std::cout << sum << "\n" << N - sum;
	return 0;
}*/