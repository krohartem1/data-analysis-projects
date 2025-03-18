/*#include <iostream>
#include <string>
#include <vector>
#include <queue>
bool substr_equality(std::vector<long long int>& powx, std::vector<long long int>& hash1, std::vector<long long int>& hash2, int L, int a, int b, int p)
{
	return(hash1[a + L - 1] + hash2[(hash1.size() - 1) - (b + L - 1)]*powx[L]) % p == (hash2[(hash1.size() - 1) - b + 1]) % p;
}
int main()
{
	long long int N, M;
	std::cin >> N >> M;
	std::vector<long long int> mirror(N+1);
	mirror[0] = 0;
	for (int i = 1; i < N + 1; ++i)
	{
		std::cin >> mirror[i];
	}
	long long int p1, p2, x1, x2;
	p1 = 1000000007;
	p2 = 1000000013; 
	x1 = 257;
	x2 = 263;
	std::vector<long long int> h1(N + 1);
	std::vector<long long int> h2(N + 1);
	std::vector<long long int> powx1(N + 1);
	h1[0] = 0;
	h2[0] = 0;
	powx1[0] = 1;
	for (size_t i = 1; i < N + 1; ++i)
	{
		h1[i] = (h1[i - 1] * x1 + mirror[i]) % p1;
		powx1[i] = (powx1[i - 1] * x1) % p1;
		h2[i] = (h2[i - 1] * x1 + mirror[N + 1 - i]) % p1;
	}
	std::priority_queue<int,std::vector<int>, std::greater<int>> pq;
	pq.push(N);
	for (int i = 1; i <= N / 2; ++i)
	{
		if (substr_equality(powx1, h1, h2, i, 1, i + 1, p1))
		{
			pq.push(N-i);
		}
	}
	while (!pq.empty()) {
		std::cout << pq.top() << " ";
		pq.pop();
	}
	return 0;
}*/