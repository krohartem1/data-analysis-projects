#include <iostream>
#include <cmath>
#include <cstdint>
#include <string>
#include <algorithm>
#include <vector>
void anagram(std::string& s1, std::string& s2)
{
	std::sort(s1.begin(), s1.end());
	std::sort(s2.begin(), s2.end());
	if (s1.size() == s2.size())
	{
		if (s1 == s2){std::cout << "YES";}
		else { std::cout << "NO"; }
	}
	else {std::cout << "NO";}
}
int main()
{
	std::string s1, s2;
	std::getline(std::cin, s1);
	std::getline(std::cin, s2);
	anagram(s1, s2);
	return 0;
}