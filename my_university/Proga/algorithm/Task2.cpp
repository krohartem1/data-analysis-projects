/*#include <vector>
#include <algorithm>
#include <iostream>
template <typename Iter>
Iter Unique(Iter first, Iter last) {
	if(first == last){return last}
	std::vector<Iter> v;
	auto it = first;
	auto it_0 = first;
	v.push_back(first);
	++it;
	for (auto it_1 = it; it_1 != last; ++it_1)
	{
		if (*it_1 != *it_0) {
			v.push_back(it_1);
			it_0 = it_1;
		}
	}
	int i = 0;
	Iter return_it = first;
	std::advance(return_it,v.size());
	for (auto it_2 = first; it_2 != return_it; ++it_2)
	{
		*it_2 = *v[i];
		++i;
	}
	return return_it;
}

int main()
{
	std::vector<int> v;//= { 5, 4, 1, 2, 3, 6, 7, 8 };
	auto iter = Unique(v.begin(), v.end());
	for (const auto& x : v)
	{
		std::cout << x << " ";
	}
	return 0;
}
*/