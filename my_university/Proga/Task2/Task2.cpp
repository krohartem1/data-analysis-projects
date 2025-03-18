#include <iostream>
#include <map>
#include <string>
#include <set>
#include <utility>
bool has_been_inserted = 0;
int main()
{
	std::map<char, int> word;
	std::set<char> set;
	std::pair<std::set<char>::iterator, bool> pair;
	int i = 0;
	std::string s;
	while (getline(std::cin, s) && s!="")
	{
		for (size_t j = 0; j < s.size(); ++j)
		{
			pair = set.insert(s[j]);
			if (pair.second)
			{
				++word[s[j]];
			}
		}
		set.clear();
		++i;
	}
	for (const std::pair<char,int> x : word)
	{
		if (x.second == i) { std::cout << x.first; }
	}
	return 0;
}