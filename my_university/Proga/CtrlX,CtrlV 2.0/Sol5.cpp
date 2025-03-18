#include <iostream>
#include <vector>
#include <string>
#include <list>
std::list<std::string> bufer;
bool shift = 0;
int t = 0;
std::list<std::string>::iterator i_0;
std::list<std::string>::iterator iter = i_0;
std::list<std::string>::iterator text_editor(std::list<std::string>& lines, std::string s0, std::list<std::string>::iterator& i)
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
	}/*
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
			bufer.clear();
			if (t > 0)
			{
				iter = i_0;
				std::advance(iter, t);
				bufer.splice(bufer.end(), lines,i_0,iter);
				lines.erase(i_0, iter);
				shift = 0;
				t = 0;
				return i_0;
			}
			else if(t < 0) {
				iter = i_0;
				for (int j = 0; j < -t; ++j)
				{
					--iter;
				}
				bufer.splice(bufer.end(), lines, iter, i_0);
				lines.erase(iter, i_0);
				shift = 0;
				t = 0;
				return iter;
			}
			else {
				if (*i != "")
				{
					bufer.push_back(*i);
					std::list<std::string>::iterator it = lines.begin();
					std::advance(it, i);
					lines.erase(it);
					shift = 0;
					return i;
				}
				else { return i; }
			}
		}
		else
		{
			if (*i != "")
			{
				bufer.push_back(*i);
				std::list<std::string>::iterator it = lines.begin();
				std::advance(it, i);
				lines.erase(it);
				return i;
			}
			else { return i; }
		}
	}
	else if (s0 == "Ctrl+V") {
		if (shift)
		{
			lines.splice(i, bufer, bufer.begin(), bufer.end());
			std::advance(i, bufer.size());
			return i;
		}
		else {
			if (bufer.empty()) { return i; }
			else {
				std::list<std::string>::iterator it = lines.begin();
				std::advance(it, i);
				lines.insert(it, *bufer.begin());
				return ++i;
			}
		}
	}
	else
	{
		shift = 1;
		i_0 = i;
		return i;
	}*/
return i;
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
	while (std::getline(std::cin, s))
	{
		i = text_editor(lines, s, i);
	}
	for (auto it = lines.begin(); it != lines.end(); ++it)
	{
		std::cout << *it << "\n";
	}
	return 0;
}