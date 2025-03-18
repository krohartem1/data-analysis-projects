#include <iostream>
#include <vector>
#include <string>
#include <list>
std::list<std::string> bufer;
bool shift = 0;
int t = 0;
std::list<std::string>::iterator i_0;
std::list<std::string>::iterator iter;
std::list<std::string>::iterator text_editor(std::list<std::string>& lines, std::string s0, std::list<std::string>::iterator i)
{
	if (s0 == "Down") {
		if (shift)
		{
			if (*i != "")
			{
				++t;
				return ++i;
			}
			else {
				return i;
			}
		}
		else {
			if (*i != "")
			{
				return ++i;
			}
			else { return i; }
		}
	}
	else if (s0 == "Up") {
		if (shift) {
			if (i != lines.begin())
			{
				--t;
				return --i;
			}
			else {
				return i;
			}
		}
		else {
			if (i != lines.begin())
			{
				return --i;
			}
			else { return i; }
		}
	}
	else if (s0 == "Ctrl+X") {
		if (shift)
		{
			shift = 0;
			if (t > 0)
			{
				bufer.clear();
				iter = i_0;
				std::advance(iter, t);
				bufer.splice(bufer.begin(), lines,i_0,iter);
				t = 0;
				i_0 = lines.end();
				return iter;
			}
			else if(t < 0) {
				bufer.clear();
				iter = i_0;
				for (int j = 0; j < -t; ++j)
				{
					--iter;
				}
				bufer.splice(bufer.begin(), lines, iter, i_0);
				t = 0;
				return i_0;
			}
			else {
				if (*i != "")
				{
					bufer.clear();
					bufer.push_back(*i);
					return lines.erase(i);
				}
				else { return i; }
			}
		}
		else
		{
			if (*i != "")
			{
				bufer.clear();
				bufer.push_back(*i);
				return lines.erase(i);
			}
			else { return i; }
		}
	}
	else if (s0 == "Ctrl+V") {
		if (bufer.empty()) { return i; }
		else{
		if (shift)
		{
			if (t > 0)
			{
				iter = i_0;
				std::advance(iter, t);
				i = lines.erase(i_0, iter);
			}
			else if (t < 0) {
				iter = i_0;
				for (int j = 0; j < -t; ++j)
				{
					--iter;
				}
				i = lines.erase(iter, i_0);
			}
			shift = 0;
			t = 0;
			lines.insert(i, bufer.begin(), bufer.end());
			return i;
		}
		else {
				lines.insert(i, bufer.begin(), bufer.end());
				return i;
			}
		}
	}
	else
	{
		shift = 1;
		i_0 = i;
		return i;
	}
}
int main()
{
	std::list<std::string> lines;
	std::string s;
	std::string null = "";
	while (std::getline(std::cin, s) && s != null)
	{
		lines.push_back(s);
	}
	lines.push_back(null);
	std::list<std::string>::iterator i = lines.begin();
	while (std::getline(std::cin, s) && s!=null)
	{
		i = text_editor(lines, s, i);
	}
	auto it_1 = lines.end();
	--it_1;
	for (auto it = lines.begin(); it != it_1; ++it)
	{
		std::cout << *it << "\n";
	}
	return 0;
}