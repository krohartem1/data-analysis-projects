/*
#include <iostream>
#include <vector>

bool exam(int col, int str, std::vector<bool>& line, std::vector<bool>& diag0, std::vector<bool>& diag1)
{
	if (line[str] == 0 && diag0[col + str] == 0 && diag1[str - col + line.size() - 1] == 0)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}

int N_N(int col, std::vector<bool>& line, std::vector<bool>& diag0, std::vector<bool>& diag1)
{
	int sum = 0;
	if (col == line.size()) {
		return 1;
	}
	for (int i = 0; i < line.size(); ++i)
	{
		if (exam(col, i, line, diag0, diag1))
		{
			line[i] = 1;
			diag0[i + col] = 1;
			diag1[i - col + line.size() - 1] = 1;
			sum += N_N(col+1,line, diag0, diag1);
			line[i] = 0;
			diag0[i + col] = 0;
			diag1[i - col + line.size() - 1] = 0;
		}
	}
	return sum;
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::vector<bool> line(N, 0);
	std::vector<bool> diag0(2 * N - 1, 0);
	std::vector<bool> diag1(2 * N - 1, 0);
	std::cout << N_N(0, line, diag0, diag1);
	return 0;
}
*/