/*#include <iostream>
#include <string>
#include <vector>
#include <string_view>

bool substr_equality(std::vector<long long int>& powx, std::vector<long long int>& hash, int L, int a, int b, int p)
{
	return(hash[a + L - 1] + hash[b - 1] * powx[L]) % p == (hash[b + L - 1] + hash[a - 1] * powx[L]) % p;
}
int main()
{
	std::string s0;
	std::getline(std::cin, s0);
	std::string s = ' ' + s0;
	long long int p1, p2, x1, x2;
	p1 = 1000000007;
	p2 = 1000000013;
	x1 = 257;
	x2 = 263;
	std::vector<long long int> h1(s.size());
	std::vector<long long int> h2(s.size());
	std::vector<long long int> powx1(s.size());
	std::vector<long long int> powx2(s.size());
	h1[0] = 0;
	h2[0] = 0;
	powx1[0] = 1;
	powx2[0] = 1;
	for (size_t i = 1; i < s.size(); ++i)
	{
		h1[i] = (h1[i - 1] * x1 + (s[i] - ' ')) % p1;
		powx1[i] = (powx1[i - 1] * x1) % p1;
		h2[i] = (h2[i - 1] * x2 + (s[i] - ' ')) % p2;
		powx2[i] = (powx2[i - 1] * x2) % p2;
	}
	int k = 0;
	for (size_t i = 1; i < s0.size(); ++i)
	{
		if (substr_equality(powx1, h1, i, 1, s.size() - i, p1) * substr_equality(powx2, h2, i, 1, s.size() - i, p2)) { k = i;}
	}
	std::cout << s0.size() - k;
	return 0;
}*/