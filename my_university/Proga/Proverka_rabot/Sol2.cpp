#include <iostream>
#include <deque>
#include <string>
#include <utility>
#include <vector>
void creating_a_queue(std::deque<std::string>& queue, std::vector<std::pair<std::string, std::string>>& v)
{
	for (auto& x : v)
	{
		if (x.second == "top") { queue.push_front(x.first); }
		else{ queue.push_back(x.first); }
	}
}
int main()
{
	size_t N = 0;
	std::cin >> N; 
	std::vector<std::pair<std::string, std::string>> v(N);
	for (size_t i = 0; i < N; ++i)
	{
		std::cin >> v[i].first >> v[i].second;
	}
	size_t M = 0;
	std::cin >> M;
	std::vector<int> numbers(M);
	for (size_t j = 0; j < M; ++j) { std::cin >> numbers[j]; }
	std::deque<std::string> queue;
	creating_a_queue(queue, v);
	for (auto x : numbers) { std::cout << queue[x - 1] << "\n"; }
	return 0;
}