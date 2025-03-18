/*#include <iostream>
#include <vector>
std::vector<int> merge(std::vector<int> first, std::vector<int> second)
{
	std::vector<int> result;
	if (first.empty() && !second.empty()) { return second; }
	else if (!first.empty() && second.empty()) { return first; }
	else if (first.empty() && second.empty()) { return result; }
	auto it1 = first.begin();
	auto it2 = second.begin();
	while (it1 != first.end() && it2 != second.end())
	{
		if (*it1 <= *it2) { result.push_back(*it1); ++it1; }
		else { result.push_back(*it2); ++it2; }
	}
	if (it1 == first.end() && it2 != second.end()) {
		for (auto it = it2; it != second.end(); ++it)
		{
			result.push_back(*it);
		}
	}
	else if (it1 != first.end() && it2 == second.end()) {
		for (auto it = it1; it != first.end(); ++it)
		{
			result.push_back(*it);
		}
	}
	return result;
}

std::vector<int> merge_sort(std::vector<int>& mass, int begin, int end)
{
	std::vector<int> result;
	if (mass.empty()) { return result; }
	else if (begin == end) {
		 result.push_back(mass[begin]);
		return result;
	}
	int k = (end + begin) / 2;
	return merge(merge_sort(mass, begin, k), merge_sort(mass, (k + 1), end));
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
	mass = merge_sort(mass, 0, N - 1);
	for (int i = 0; i < mass.size(); ++i)
	{
		std::cout << mass[i] << " ";
	}
	return 0;
}*/