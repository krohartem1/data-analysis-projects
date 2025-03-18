/*
#include <vector>
#include <iostream>
#include <map>
#include <tuple>
#include <utility>
#include<iomanip>
#include <queue>
#include <cstdint>
#include <fstream>
double L = 100000000;
void Dijkstroy_bypass(std::map<int, std::vector<std::pair<int, int>>>& graph, std::vector<double>& best_dist_k, std::vector<std::pair<double, double>>& yam, int k)
{
	std::queue<int> q;
	std::vector<bool> visited(yam.size(), 0);
	q.push(k);
	int next_vertex = 0;
	int min_time_k = 1000000000;
	int	j = 0;;
	best_dist_k[k] = 0;
	while (!q.empty())
	{
		next_vertex = q.front();
		if (visited[next_vertex]) { q.pop(); }
		else
		{
			q.pop();
			visited[next_vertex] = 1;
			for (std::pair<int, int>& p : graph[next_vertex])
			{
				if (visited[p.first]) { continue; }
				else
				{
					best_dist_k[p.first] = best_dist_k[next_vertex] + p.second;
					q.push(p.first);
				}
			}
		}
	}
}
std::pair<double, int> algorithm_Dijkstra(std::map<int, std::vector<std::pair<int, int>>>& graph, std::vector<std::pair<double, double>>& yam, std::vector<int>& reduction, int S)
{
	std::vector<double> best_dist_k(yam.size(), 0);
	std::vector<bool> visited(yam.size(), 0);
	std::vector<double> dist(yam.size(), L);
	dist[S] = 0;
	std::priority_queue < std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<std::pair<int, int>>> pq;
	pq.push({ 0, S });
	bool change = 1;
	double min_time_k = 1000000000;
	int j = 0;
	int next_vertex = 0;
	int prev = 0;
		while (change)
		{
			next_vertex = -1;
			for (size_t i = 1; i < yam.size(); ++i)
			{
				if (visited[i] == 0)
				{
					next_vertex = i;
					i = yam.size();
				}
			}
			if (next_vertex == -1 || pq.empty()) { change = 0; break; }
			next_vertex = pq.top().second;
			Dijkstroy_bypass(graph, best_dist_k, yam, next_vertex);
			if (visited[next_vertex]) { pq.pop(); }
			else {
				pq.pop();
				visited[next_vertex] = 1;
				for (size_t i = 1; i < best_dist_k.size(); ++i)
				{
					if (visited[i] == 0 && dist[i] > (best_dist_k[i] / yam[i].second) + yam[i].first  + dist[next_vertex])
					{
						dist[i] = (best_dist_k[i] / yam[i].second)  + yam[i].first + dist[next_vertex];
						reduction[i] = next_vertex;
					}
					if (visited[i] == 0 && min_time_k > dist[i])
					{
						min_time_k = dist[i];
						j = i;
					}
				}
				pq.push({ dist[j],j });
			}
			prev = next_vertex;
			min_time_k = 1000000000;
			j = 0;
		}
	return { dist[prev], prev };
}

int main() {
	int N;
	std::cin >> N;
	//std::ifstream in("Test8.txt");
	int T, V;
	std::vector<std::pair<double, double>> yam(N + 1);
	for (int i = 1; i < N + 1; ++i)
	{
		std::cin >> T >> V;
		yam[i] = { T, V };
	}
	int A, B, S;
	std::map<int, std::vector<std::pair<int, int>>> graph;
	for (int i = 0; i < N - 1; ++i)
	{
		std::cin >> A >> B >> S;
		graph[A].push_back({ B, S });
		graph[B].push_back({ A, S });
	}
	std::vector<int> reduction(yam.size(), 1);
	std::pair<double, int> p = algorithm_Dijkstra(graph, yam, reduction, 1);
	double q = p.first;
	std::cout << std::setprecision(10) << q << "\n";
	std::vector<int> normal_reduction;
	int x = p.second;
	while (x != 1)
	{
		normal_reduction.push_back(x);
		x = reduction[x];
	}
	normal_reduction.push_back(1);
	for(auto it = normal_reduction.begin(); it != normal_reduction.end(); ++it)
	{
		std::cout << *it << " ";
	}
	return 0;
}
*/