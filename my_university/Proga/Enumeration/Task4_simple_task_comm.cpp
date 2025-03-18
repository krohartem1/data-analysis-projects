/*
#include <iostream>
#include <vector>
#include <map>
#include <utility>
int Sum  = -1;
bool min_dist_cycle(std::vector<std::vector<int>>& matrix, int min_edge, std::vector<bool> visited, int visit_vertex, int vertex, int sum)
{
	visited[vertex] = 1;
	if (visit_vertex == matrix.size())
	{
		if (matrix[vertex][0] != 0 && (Sum == -1 ||Sum > sum + matrix[vertex][0]))
		{
			Sum = sum + matrix[vertex][0];
			return 1;
		}
	}
	int next = -1;
	for (int i = 0; i < matrix[vertex].size(); ++i)
	{
		if (matrix[vertex][i] != 0 && visited[i] != 1)
		{
			if (sum + (matrix.size() - visit_vertex) * min_edge > Sum && Sum != -1)
			{
				return 1;
			}
			else
			{
				next = i;
				visited[i] = 1;
				sum += matrix[vertex][i];
				min_dist_cycle(matrix, min_edge, visited, visit_vertex + 1, i, sum);
				visited[i] = 0;
				sum -= matrix[vertex][i];
			}
		}
	}
	if (next == -1)
	{
		return 1;
	}
}

int main()
{
	int N = 0;
	std::cin >> N;
	int min_edge = -1;
	std::vector<std::vector<int>> matrix(N, std::vector<int>(N));
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < N; ++j)
		{
			std::cin >> matrix[i][j];
			if (min_edge == -1 && matrix[i][j] > 0)
			{
				min_edge = matrix[i][j];
			}
			 else if (matrix[i][j] > 0 && min_edge > matrix[i][j])
			{
				min_edge = matrix[i][j];
			}
		}
	}
	std::vector<bool> visited(N, 0);
	min_dist_cycle(matrix, min_edge, visited, 1, 0, 0);
	if (N == 1) { std::cout << 0; }
	else { std::cout << Sum; }
	return 0;
}
*/