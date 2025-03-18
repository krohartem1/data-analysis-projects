#include <iostream>
#include <string>
#include <set>
#include <algorithm>
int main()
{
	std::set<std::string> dir;
	std::string s;
	while (std::getline(std::cin, s) && s!="")
	{
		int pos = 0;
		size_t pos1 = s.find("/", 1);
		std::string s1 = ""; s1 += s[pos]; dir.insert(s1);
		while (pos1 < s.size())
		{
			dir.insert(s.substr(pos, pos1 + 1));
			pos1 = s.find("/", pos1 + 1);
		}
	}
	for (const auto& str : dir)
	{
		std::cout << str << "\n";
	}
}