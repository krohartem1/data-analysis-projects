/*#include <iostream>
#include <vector>
#include <map>
#include <utility>
#include<list>
std::vector<int> algorithm_Dijkstra(std::map<int, std::vector<std::pair<int, int>>>& graph, int S, int F)
{
	std::vector<bool> visited(graph.size() + 1, 0);
	std::vector<int> dist(graph.size() + 1, 1000);
	std::vector<int> reduction(graph.size() + 1, -1);
	dist[S] = 0;
	bool change = 1;
	int next_vertex = 0;
	if (!graph[S].empty())
	{
		while (change)
		{
			next_vertex = -1;
			int min = 1000;
			for (int i = 1; i < graph.size() + 1; ++i)
			{
				if (visited[i] == 0 && min > dist[i])
				{
					min = dist[i];
					next_vertex = i;
				}
			}
			if (next_vertex == -1) { change = 0; break; }
			visited[next_vertex] = 1;
			for (int i = 0; i < graph[next_vertex].size(); ++i)
			{
				if (dist[graph[next_vertex][i].first] > graph[next_vertex][i].second + dist[next_vertex])
				{
					dist[graph[next_vertex][i].first] = graph[next_vertex][i].second + dist[next_vertex];
					reduction[graph[next_vertex][i].first] = next_vertex;
				}
			}
		}
	}
	if (dist[F] == 1000) { return reduction; }
	else { reduction[0] = dist[F]; return reduction; }
}

int main() {
	int N, S, F;
	std::cin >> N >> S >> F;
	std::map<int, std::vector<std::pair<int, int>>> graph;
	std::vector<std::vector<int>> matrix(N, std::vector<int>(N));
	for (int i = 0; i < N; ++i)
	{
		for (int j = 0; j < N; ++j)
		{
			std::cin >> matrix[i][j];
			if (matrix[i][j] != 0 && matrix[i][j] != -1)
			{
				graph[i + 1].push_back({ j + 1, matrix[i][j] });
			}
			else
			{
				graph[i + 1];
			}
		}
	}
	std::vector<int> reduction; 
	if (algorithm_Dijkstra(graph, S, F)[0] == -1) {
		std::cout << -1;
	}
	else
	{
		reduction.push_back(F);
		int x = algorithm_Dijkstra(graph, S, F)[F];
		while (x != -1)
		{
			reduction.push_back(x);
			x = algorithm_Dijkstra(graph, S, F)[x];
		}
	}
	for (size_t i = 0; i < reduction.size(); ++i)
	{
		std::cout << reduction[reduction.size() - i - 1] << " ";
	}
	return 0;
}*/