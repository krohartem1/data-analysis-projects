#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <utility>

void NOT_MIN(const std::vector<int>& m, int a, int b)
{
	std::set<int> s;
	for (int i = a; i <= b; ++i)
	{
		s.insert(m[i]);
	}
	int setint = *s.begin();
	s.erase(setint);
	if (s.empty())
	{
		std::cout << "NOT FOUND" << "\n";
	}
	else
	{
		std::cout << *s.begin() << "\n";
	}
}
int main()
{
	size_t N = 0;
	size_t M = 0;
	std::cin >> N >> M;
	std::vector <int> numbers;
	int x = 0;
	for (size_t i = 0; i < N; ++i)
	{
		std::cin >> x;
		numbers.push_back(x);
	}
	std::vector<std::pair<int, int>> A(M);
	for (size_t i = 0; i < M; ++i)
	{
		std::cin >> A[i].first >> A[i].second;
	}
	for (size_t i = 0; i < M; ++i)
	{
		NOT_MIN(numbers, A[i].first, A[i].second);
	}
    return 0;
} 