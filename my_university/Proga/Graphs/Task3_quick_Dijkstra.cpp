/*#include <iostream>
#include <vector>
#include <map>
#include <utility>
#include<list>
#include <queue>
#include <cstdint>
#include <fstream>
uint64_t L = 1000000000000;
class CompareDist
{
public:
	bool operator()(std::pair<int64_t, int64_t> p1, std::pair<int64_t, int64_t> p2) {
		return std::tie(p1.first, p1.second) > std::tie(p2.first, p2.second);
	}
};
int64_t algorithm_Dijkstra(std::map<int, std::vector<std::pair<int, int>>>& graph, int S, int F)
{
	std::vector<bool> visited(graph.size() + 1, 0);
	std::vector<uint64_t> dist(graph.size() + 1, L);
	dist[S] = 0;
	std::priority_queue < std::pair<int64_t, int64_t>, std::vector<std::pair<int64_t, int64_t>>, CompareDist> pq;
	pq.push({0, S});
	bool change = 1;
	int next_vertex = 0;
	if (!graph[S].empty())
	{
		while (change)
		{
			//next_vertex = -1;
			//for (int i = 1; i < graph.size() + 1; ++i)
			//{
				//if (visited[i] == 0)
				//{
					//next_vertex = i;
					//i = graph.size() + 1;
				//}
			//}
			if (pq.empty()) { change = 0; break; }
			next_vertex = pq.top().second;
			pq.pop();
			visited[next_vertex] = 1;
			for (int i = 0; i < graph[next_vertex].size(); ++i)
			{
				if (dist[graph[next_vertex][i].first] > graph[next_vertex][i].second + dist[next_vertex])
				{
					dist[graph[next_vertex][i].first] = graph[next_vertex][i].second + dist[next_vertex];
					pq.push({ dist[graph[next_vertex][i].first] ,graph[next_vertex][i].first});
				}
			}
		}
	}
	if (dist[F] == L) { return -1; }
	else { return dist[F]; }
}

int main() {
    int N, K;
	std::cin >> N >> K;
	//std::ifstream in("Test8.txt");
	std::map<int, std::vector<std::pair<int, int>>> graph;
	int64_t a, b, l;
	for (int i = 0; i < K; ++i)
	{
		std::cin >> a >> b >> l;
		graph[a].push_back({ b, l });
		graph[b].push_back({ a, l });
	}
	for (int i = 1; i < N + 1; ++i)
	{
		if (!graph[i].empty()) {}
		else {
			graph[i];
		}
	}
	int A, B;
	std::cin >> A >> B;
	std::cout << algorithm_Dijkstra(graph, A, B);
	return 0;
}*/