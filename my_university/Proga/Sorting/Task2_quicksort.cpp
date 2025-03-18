/*
#include <iostream>
#include <vector>
#include <string>
#include<utility>
std::pair<std::vector<int>::iterator, std::vector<int>::iterator> partition(std::vector<int>& mass, int x, std::vector<int>::iterator begin, std::vector<int>::iterator end)
{
	std::pair<std::vector<int>::iterator, std::vector<int>::iterator> p;
	if (begin == end || mass.empty()) {p.first = end; p.second = end; return p; }
	auto G = begin;
	auto P = begin;
	if (*begin < x)
	{
		P = std::next(begin);
		G = std::next(begin);
	}
	else if (*begin == x)
	{
		G = std::next(begin);
	}
	for (auto it = ++begin; it != end; ++it)
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
	p.first = P;
	p.second = G;
	return p;
}

bool quicksort(std::vector<int>& mass, std::vector<int>::iterator begin, std::vector<int>::iterator end)
{
	if (begin == end) { return 1;}
	if (std::next(begin) == end) { return 1;}
	std::pair<std::vector<int>::iterator, std::vector<int>::iterator> p;
	srand(time(NULL));
	int x = mass[(begin - mass.begin()) + rand()%((end - mass.begin())- (begin - mass.begin()))];
	p = partition(mass, x, begin, end);
	quicksort(mass,begin,p.first);
	quicksort(mass, p.second, end);
	return 1;
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::vector<int> mass(N);
	for (int i = 0; i < N; ++i)
	{
		std::cin >> mass[i];
	}
	quicksort(mass, mass.begin(), mass.end());
	for (const auto& x : mass)
	{
		std::cout << x << " ";
	}
}
*/