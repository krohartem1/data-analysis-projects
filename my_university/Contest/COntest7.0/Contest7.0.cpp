#include <iostream>
#include <cstdint>
#include <vector>
#include <cmath>
void product_line(std::vector<std::vector<int>>& product_matrix, int i, std::vector<std::vector<int>>& matrix)
{
		for (int k = 0; k < matrix[0].size(); ++k)
		{
			product_matrix[i][k] += matrix[i][k];
			for(int j = i + 1; j < matrix.size(); ++j)
			{
				if (matrix[i][k] == 1 && matrix[j][k] == 1)
				{
					++product_matrix[i][k];
				}
				else { break;}
			}
		}
}
int square_of_carrots(std::vector<std::vector<int>>& matrix)
{
	int Size = 0;
	int final_size = 0;
	std::vector<std::vector<int>> product_matrix(matrix.size(), std::vector<int>(matrix[0].size()));
	int j_0 = 0;
	int j_1 = 0;
	for (int l = 0; l < matrix.size(); ++l)
	{
		product_line(product_matrix, l, matrix);
			while (j_0 != matrix[0].size())
			{
				if (product_matrix[l][j_0] <= final_size || product_matrix[l][j_0] + l > matrix.size()) { ++j_0; }
				else {
					int p = product_matrix[l][j_0];
					j_1 = j_0;
					while (j_1 < matrix[0].size() && product_matrix[l][j_0] != 0 && j_1 - j_0 < product_matrix[l][j_1] && j_1 - j_0 + 1 <=std::min(p, product_matrix[l][j_0]))
					{
						if (p > product_matrix[l][j_1]) { p = product_matrix[l][j_1];}
						++j_1;
					}
					Size = j_1 - j_0;
					++j_0;
					if (final_size < Size)
					{
						final_size = Size;
					}
				}
			}
			j_0 = 0;
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