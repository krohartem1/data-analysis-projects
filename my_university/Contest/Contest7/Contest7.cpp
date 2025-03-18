#include <iostream>
#include <cstdint>
#include <vector>
#include <cmath>
bool submatrix_square_test(int i,int j_0, int j_1, std::vector<std::vector<int>>& matrix)
{
	if (j_0 == j_1 && matrix[i][j_0] == 1) { return 1; }
	else if (j_0 == j_1 && matrix[i][j_0] == 0) { return 0;}
	int side = j_1 - j_0 + 1;
	int N_0 = matrix.size();
	int M_0 = matrix[0].size();
	if (i + side > N_0)
	{
		return 0;
	}
	else
	{
		for (int k = i; k < i + side; ++k)
		{
			for (int l = j_0; l <= j_1; ++l)
			{
				if(matrix[k][l] == 0)
				{
					return 0;
				}
			}
		}
		return 1;
	}
}
int square_of_carrots(std::vector<std::vector<int>>& matrix)
{
	int maxsize = std::min(matrix.size(), matrix[0].size());
	int final_size = 0;
	int Size = 0;
	int maxside = 0;
	int j_0 = 0;
	int j_1 = 0;
	for (int i = 0; i < matrix.size(); ++i)
	{
		while (j_0 != matrix[0].size())
		{
			if (matrix[i][j_0] == 1)
			{
				j_1 = j_0;
				while (j_1 + 1 < matrix[0].size() &&  matrix[i][j_1 + 1] == 1)
				{
					++j_1;
				}
				maxside = j_1 - j_0 + 1;
				if (final_size >= maxside) { break; }
				bool I = submatrix_square_test(i, j_0, j_1, matrix);
				while (!I)
				{
					--j_1;
					int j = maxside - j_1 + j_0 - 1;
					for (int k = 0; k <= j; ++k)
					{
						I = submatrix_square_test(i, j_0 + k, j_1 + k, matrix);
						if (I) { break; }
					}
				}
				Size = j_1 - j_0 + 1;
				if (Size == maxsize) { return Size; }
				if (final_size < Size) { final_size = Size; }
				j_0 += maxside;
			}
			else
			{
				++j_0;
			}
		}
		Size = 0;
		j_0 = 0;
		j_1 = 0;
	}
	return final_size;
}
int main()
{
	size_t N, M;
	std::cin >> N >> M;
	std::vector<std::vector<int>>matrix(N, std::vector<int>(M));
	for (size_t i = 0; i < N; ++i)
	{
		for (size_t j = 0; j < M; ++j)
		{
			std::cin >> matrix[i][j];
		}
	}
	std::cout << square_of_carrots(matrix);
	return 0;
}