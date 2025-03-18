/*#include <iostream>
#include <string>

std::string enumer(std::string s, std::string s_)
{
	if (s.empty()) { std::cout << s_ << "\n"; return s_; }
	else
	{
		for (size_t i = 0; i < s.size(); ++i)
		{
			std::string s0 = s.substr(0, i) + s.substr(i+1);
			s_ += s[i];
			s_ = enumer(s0, s_);
			s_.pop_back();
		}
		return s_;
	}
}

int main()
{
	int N = 0;
	std::cin >> N;
	std::string s = "0123456789";
	std::string s0 = s.substr(1, N);
	enumer(s0, "");
	return 0;
}*/