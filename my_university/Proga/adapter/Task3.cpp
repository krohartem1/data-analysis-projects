/*#include <iostream>
#include <queue>
#include <string>

void processing(std::string s, std::priority_queue<int>& q)
{
	if (s == "CLEAR")
	{
		q = std::priority_queue<int>();
	}
	else if (s == "EXTRACT")
	{
		if (q.empty())
		{
			std::cout << "CANNOT\n";
		}
		else {
			std::cout << q.top() << "\n";
			q.pop();
		}
	}
	else
	{
		int x = 0;
		std::cin >> x;
		q.push(x);
	}
}

int main()
{
	std::string s;
	std::priority_queue<int> q;
	while (std::cin >> s && s!="")
	{
		processing(s, q);
	}
	return 0;
}*/