#include <iostream>
#include <map>
#include <string>
#include <set>
#include <utility>
#include <utility>
int main()
{
	size_t n = 0;
	std::cin >> n;
	std::map<int, std::set<std::string>> key_word;
	std::pair<std::string, int> pair;
	for(size_t i = 0; i < n; ++i)
	{
		std::cin >> pair.first >> pair.second;
		key_word[pair.second].insert(pair.first);
	}
	std::pair<int, std::set<std::string> > pair1;
	for (const auto& pair1 : key_word)
	{
		std::cout << pair1.first;
		for (const auto& x : pair1.second)
		{
			std::cout << " " << x;
		}
		std::cout << "\n";
	}
	return 0;
}