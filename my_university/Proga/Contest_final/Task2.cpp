/*#include <iostream>
#include <string>
#include <vector>
bool substr_equality(std::vector<long long int>& powx, std::vector<long long int>& hash1, std::vector<long long int>& hash2, int L, int a, int b, int p)
{
	return(hash1[a + L - 1] + hash2[(hash1.size() - 1) - b] * powx[L]) % p == (hash2[(hash1.size() - 1) - (b - L)] + hash1[a - 1] * powx[L]) % p;
}

int max_length_mirror(std::vector<long long int>& powx, std::vector<long long int>& hash1, std::vector<long long int>& hash2, int L, int a, int b, int p)
{
	if (L == 1)
	{
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
	if (substr_equality(powx, hash1, hash2, k, a, b, p))
	{
		sum+= k + max_length_mirror(powx, hash1, hash2, L - k, a + k, b - k, p);
	}
	else
	{
		sum += max_length_mirror(powx, hash1, hash2, L - k, a, b, p);
	}
	return sum;
}
int main()
{
	int N = 0;
	std::cin >> N;
	std::string s0;
	std::cin >>  s0;
	std::string s = ' ' + s0;
	long long int p1, p2, x1, x2;
	p1 = 1000000007;
	p2 = 1000000013;
	x1 = 257;
	x2 = 263;
	std::vector<long long int> h1(s.size());
	std::vector<long long int> h2(s.size());
	std::vector<long long int> powx1(s.size());
	std::vector<int> z(N+1);
	h1[0] = 0;
	h2[0] = 0;
	powx1[0] = 1;
	for (size_t i = 1; i < s.size(); ++i)
	{
		h1[i] = (h1[i - 1] * x1 + (s[i] - ' ')) % p1;
		powx1[i] = (powx1[i - 1] * x1) % p1;
		h2[i] = (h2[i - 1] * x1 + (s[s.size() - i] - ' ')) % p1;
	}
	for (int i = 1; i < N + 1; ++i)
	{
		z[i] = max_length_mirror(powx1, h1, h2, i, 1, i, p1);
	}
	for (int i = 1; i < N + 1; ++i)
	{
		std::cout << z[i] << " ";
	}
	return 0;
}
*/