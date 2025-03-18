/*
#include <vector>
#include<list>
#include<deque>
#include <algorithm>
#include <iostream>
template <typename InIter1, typename InIter2, typename OutIter>
OutIter SetDifference(InIter1 first1, InIter1 last1, InIter2 first2, InIter2 last2, OutIter out)
{
	InIter1 it1 = first1;
	InIter2 it2 = first2;
	OutIter result = out;
	while (it1 != last1)
	{
		if (it2 == last2)
		{
			result = std::copy(it1, last1, result);
			it1 = last1;
		}
		else {
			if (*it2 < *it1) {
				++it2;
			}
			else if (*it2 > *it1) {
				*result = *it1;
				++result;
				++it1;
			}
			else {
				++it2;
				++it1;
			}
		}
	}
	return result;
}
int main()
{
	std::vector<int> in1 = { 1, 3, 5, 5, 7 };
	std::list<int> in2 = { 1, 1, 2, 3 };
	std::deque<int> out;
	SetDifference(in1.begin(), in1.end(),
		in2.begin(), in2.end(),
		std::back_inserter(out));
	for (const auto& x : out)
	{
		std::cout << x << " ";
	}
	return 0;
}*/