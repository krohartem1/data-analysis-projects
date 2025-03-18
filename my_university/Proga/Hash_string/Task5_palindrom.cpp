/*#include <iostream>
#include <string>
#include <vector>
bool substr_equality(std::vector<long long int>& powx, std::vector<long long int>& hash1, std::vector<long long int>& hash2, int L, int a, int b, int p)
{
	return(hash1[a + L - 1] + hash2[(hash1.size() - 1) - (b + L - 1)] * powx[L]) % p == (hash2[(hash1.size() - 1) - b + 1] + hash1[a - 1] * powx[L]) % p;
}
int max_palindrom(std::vector<long long int>& powx, std::vector<long long int>& hash1, std::vector<long long int>& hash2, int L, int a, int b, int p)
{
	if (L == 1) {
		if (substr_equality(powx, hash1, hash2, L, a, b, p))
		{
			return 1;
		}
		else
		{
			return 0;
		}
	}
	int sum = 0;
	int k = L / 2;
	if (substr_equality(powx, hash1, hash2, k, a - k + 1, b, p))
	{
		sum += k + max_palindrom(powx, hash1, hash2, L-k, a - k, b + k, p);
	}
	else
	{
		sum += max_palindrom(powx, hash1, hash2, L - k, a, b, p);
	}
	return sum;
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
	h1[0] = 0;
	h2[0] = 0;
	powx1[0] = 1;
	for (size_t i = 1; i < s.size(); ++i)
	{
		h1[i] = (h1[i - 1] * x1 + (s[i] - ' ')) % p1;
		powx1[i] = (powx1[i - 1] * x1) % p1;
		h2[i] = (h2[i - 1] * x1 + (s[s.size() - i] - ' ')) % p1;
	}
	int Sum = s0.size();
	int L = s0.size();
	if (substr_equality(powx1, h1, h2, 1, 1, 2, p1)) { Sum += 1; }
	for (int i = 2; i < s0.size(); ++i)
	{
		int L1 = std::min(i - 1, L - i);
		int L2 = std::min(i, L - i);
		Sum += max_palindrom(powx1, h1, h2, L1, i - 1, i + 1, p1) + max_palindrom(powx1, h1, h2, L2, i, i + 1, p1);
	}
	std::cout << Sum;
	return 0;
}*/
