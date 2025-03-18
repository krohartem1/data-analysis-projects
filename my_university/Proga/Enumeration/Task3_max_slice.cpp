/*
#include <iostream>
#include <vector>
#include <map>
#include <utility>
int check(std::vector<std::vector<int>>& matrix, std::vector<int>& INITIALIZER)
{
	int Sum = 0;
	for (size_t i = 0; i < matrix.size(); ++i)
	{
		for (size_t j = i; j < matrix[0].size(); ++j)
		{
			if (INITIALIZER[i] != INITIALIZER[j])
			{
				Sum += matrix[i][j];
			}
		}
	}
	return Sum;
}

bool enumer(std::vector<std::vector<int>>& matrix, std::vector<int>& INITIALIZER, int index, int k, int& Sum, std::vector<int>& initial)
{
	if (index == matrix.size())
	{
		int Sum0 = check(matrix, INITIALIZER);
		if (Sum < Sum0) { Sum = Sum0; initial = INITIALIZER; }
	}
	else if (index < matrix.size())
	{
		INITIALIZER[index] = k;
		enumer(matrix, INITIALIZER, index + 1, 1, Sum, initial);
		enumer(matrix, INITIALIZER, index + 1, 2, Sum, initial);
	}
	return 1;
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::vector<std::vector<int>> matrix(N, std::vector<int>(N));
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < N; ++j)
		{
			std::cin >> matrix[i][j];
		}
	}
	std::vector<int> INITIALIZER(N, 1);
	int Sum = 0;
	std::vector<int> initial(N);
	enumer(matrix, INITIALIZER, 0, 1, Sum, initial);
	std::cout << Sum << "\n";
	for (int i = 0; i < N; ++i)
	{
		std::cout << initial[i] << " ";
	}
	return 0;
}
*/