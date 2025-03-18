/*
#include<iostream>
#include<cstdint>

int main()
{
	int x = 0;
	std::cin >> x;
	uint64_t a_i, b_j;
	int i = 1;
	int j = 1;
	a_i = 1;
	b_j = 1;
	uint64_t result = 1;
	while (x != 0)
	{
		if (a_i == b_j)
		{
			result = a_i;
			++i;
			++j;
			a_i = i*i;
			b_j = j*j*j;
		}
		else if (a_i < b_j)
		{
			result = a_i;
			++i;
			a_i = i*i;
		}
		else if (a_i > b_j)
		{
			result = b_j;
			++j;
			b_j = j*j*j;
		}
		--x;
	}
	std::cout << result;
	return 0;
}
*/