#include <iostream>
#include <list>
#include <string>
#include <utility>
void MakeTrain()
{
	std::string s;
	std::pair<std::string, int>pair;
	std::list<int> train;
	while (std::cin >> pair.first >> pair.second)
	{
		//size_t pos1 = s.find(' ');
		//pair.first = s.substr(0, pos1);
		//pair.second = s[pos1 + 1] - '0';
		if (pair.first == "+left") { train.push_front(pair.second); }
		else if (pair.first == "+right") { train.push_back(pair.second); }
		else if (pair.first == "-left") {
			int size = train.size();
			if (size <= pair.second) { train.clear(); }
			else {
				auto it = train.begin();
				std::advance(it, pair.second);
				train.erase(train.begin(), it);
			}
		}
		else if (pair.first == "-right") {
			int size = train.size();
			if (size <= pair.second) { train.clear(); }
			else {
				auto it = train.begin();
				std::advance(it,size - pair.second);
				auto it1 = train.end();
				train.erase(it, it1);
			}
		}
		else { break; }
	}
	for (auto& x : train)
	{
		std::cout << x << " ";
	}
}

int main()
{
	MakeTrain();
	return 0;
}