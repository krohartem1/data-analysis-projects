#include <iostream>
#include <cstdint>
#include <vector>
#include <cmath>
int main()
{
	int Size = 0;
	int final_size = 0;
	int j_0 = 0;
	int j_h = 0;
	int j_h_min = 0;
	int h_min = 1001;
	int h = 1001;
	int len = 0;
	size_t N, M;
	std::cin >> N >> M;
	std::vector<std::vector<int>>matrix(N + 1, std::vector<int>(M + 2));
	for (size_t i = 1; i < N + 1; ++i)
	{
		for (size_t j = 1; j < M + 1; ++j)
		{
			std::cin >> matrix[i][j];
			matrix[i][j] += matrix[i][j] * matrix[i - 1][j];
			if (h_min >= matrix[i][j]) { h_min = matrix[i][j]; j_h_min = j; h = 1001; j_h = j_h_min;}
			else if (matrix[i][j] < h) { h = matrix[i][j]; j_h = j;}
			if (matrix[i][j] != 0)
			{
				++len;
				if (len >= h_min)
				{
					Size = h_min;
					len -= j_h_min - j_0;
					j_0 = j_h_min;
					j_h_min = j_h; 
					h_min = matrix[i][j_h_min]; 
					h = 1001;
				}
			}
			else { len = 0; j_0 = j; h_min = 1001; h = 1001; }
			if (final_size < Size) { final_size = Size; }
		}
		len = 0;
		h_min = 1001;
		h = 1001;
		j_0 = 0;
		j_h = 0;
	}
	std::cout << final_size;
	return 0;
}