#include <iostream>
#include<vector>
#include <utility>
#include<queue>
const int INF = 1e9 + 7;
const int MAXN = 1e5 + 5;
std::vector<std::pair<int, std::pair<int, int>>> graph[MAXN];
int dist[MAXN];

bool dijkstra(int start, int mid, int n) {
	std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>,
		std::greater<std::pair<int, int>>>
		pq;
	std::fill(dist, dist + n + 1, INF);
	dist[start] = 0;
	pq.push({ 0, start });

	while (!pq.empty()) {
		int node = pq.top().second;
		int time = pq.top().first;
		pq.pop();

		if (time != dist[node]) continue;

		for (auto& edge : graph[node]) {
			int adj = edge.first;
			int adj_time = edge.second.first;
			int cup = edge.second.second;

			if (cup >= mid && time + adj_time < dist[adj]) {
				dist[adj] = time + adj_time;
				pq.push({ dist[adj], adj });
			}
		}
	}

	return dist[n] <= 1440;
}

int main() {
	int n, m;
	std::cin >> n >> m;

	int min_cups = INF, max_cups = -1;
	for (int i = 0; i < m; i++) {
		int a, b, t, w;
		std::cin >> a >> b >> t >> w;
		int cup = (w - 3000000) / 100;

		min_cups = std::min(cup, min_cups);
		max_cups = std::max(cup, max_cups);

		graph[a].push_back({ b, {t, cup} });
		graph[b].push_back({ a, {t, cup} });
	}

	if (n == 1) {
		std:: cout << 10000000 << "\n";
	}
	else {
		int left = 0, right = max_cups;
		while (left <= right) {
			int mid = (left + right) / 2;
			if (dijkstra(1, mid, n)) {
				left = mid + 1;
			}
			else {
				right = mid - 1;
			}
		}
		std::cout << std::max(right, 0) << "\n";
	}
	return 0;
}
