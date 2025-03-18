#include<iostream>
#include<map>
#include<string>
#include<algorithm>
#include<utility>
#include<vector>
int main()
{
	int k = 0;
	std::cin >> k;
	std::map<std::string, int> word_freq;
	std::string s;
	while (std::cin >> s)
	{
		++word_freq[s];
	}
	std::vector<std::pair<std::string, int>> word_freq_v(word_freq.begin(), word_freq.end());
	word_freq.clear();
	std::sort(word_freq_v.begin(), word_freq_v.end(), [](const auto& p1, const auto& p2) {return std::tie(p2.second, p1.first) < std::tie(p1.second, p2.first); });
	auto iter = word_freq_v.begin();

	if (k > word_freq_v.size())
	{
		iter = word_freq_v.end();
	}
	else
	{
		std::advance(iter, k + 1);
	}
	int l = 0;
	for (const std::pair<std::string,int>& p : word_freq_v)
	{
		if (l == k) { break; }
		std::cout << p.first << "\t" << p.second << "\n";
		++l;
	}
	return 0;
}