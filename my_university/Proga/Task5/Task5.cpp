#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <utility>
#include <algorithm>
int main()
{
	size_t n, m;
	std::cin >> m >> n;
	std::map<std::string, int> word_freq;
	std::string word;
	for (size_t i = 0; i < m; ++i)
	{
		std::cin >> word;
		size_t len = word.size();
		if (len < n) { continue; }
		else {
			for (size_t j = 0; j <= len - n; ++j)
			{
				++word_freq[word.substr(j,n)];
			}
		}
	}
	std::vector<std::pair<std::string, int>> word_freq_vector(word_freq.begin(), word_freq.end());
	std::sort(word_freq_vector.begin(), word_freq_vector.end(), [](const std::pair<std::string, int>& pair1, const std::pair<std::string, int>& pair2) {return std::tie(pair2.second, pair1.first) < std::tie(pair1.second, pair2.first); });
	for (const std::pair<std::string, int>& x : word_freq_vector)
	{
		std::cout << x.first << " - " << x.second << "\n";
	}
	return 0;
}