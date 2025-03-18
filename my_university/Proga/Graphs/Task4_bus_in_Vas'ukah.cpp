#include <iostream>
#include <vector>
#include <map>
#include <tuple>
#include <utility>
#include<list>
#include <queue>
#include <cstdint>
#include <fstream>
uint64_t L = 100000;
class CompareDist
{
public:
	bool operator()(std::pair<int64_t, int64_t> p1, std::pair<int64_t, int64_t> p2) {
		return std::tie(p1.first, p1.second) > std::tie(p2.first, p2.second);
	}
};
int64_t algorithm_Dijkstra(std::map<int, std::vector<std::tuple<int, int, int>>>& graph, int S, int F)
{
	std::vector<bool> visited(graph.size() + 1, 0);
	std::vector<uint64_t> dist(graph.size() + 1, L);
	dist[S] = 0;
	std::priority_queue < std::pair<int64_t, int64_t>, std::vector<std::pair<int64_t, int64_t>>, CompareDist> pq;
	pq.push({ 0, S });
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
				if (dist[std::get<1>(graph[next_vertex][i])] > std::get<0>(graph[next_vertex][i]))
				{
					dist[std::get<1>(graph[next_vertex][i])] = std::get<2>(graph[next_vertex][i]);
					pq.push({ dist[std::get<1>(graph[next_vertex][i])] ,std::get<1>(graph[next_vertex][i])});
				}
			}
		}
	}
	if (dist[F] == L) { return -1; }
	else { return dist[F]; }
}

int main() {
	int N;
	std::cin >> N;
	//std::ifstream in("Test8.txt");
	int d, v;
	std::cin >> d >> v;
	int R = 0;
	std::cin >> R;
	int A, B, t1, t2;
	std::map<int, std::vector<std::tuple<int, int, int>>> graph;
	for (int i = 0; i < R; ++i)
	{
		std::cin >> A >> t1 >> B >> t2;
		graph[A].push_back({t1, B, t2 });
	}
	for (int i = 1; i < N + 1; ++i)
	{
		if (!graph[i].empty()) {}
		else {
			graph[i];
		}
	}
	std::cout << algorithm_Dijkstra(graph, d, v);
	return 0;
}