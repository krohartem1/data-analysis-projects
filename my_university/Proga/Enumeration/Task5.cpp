#include <iostream>
#include <vector>
#include <string>
#include <stack>
void generate(std::string s, int n, int len, std::stack<char> seq)
{
	if (s[len - 1] == '(' || s[len - 1] == '[')
	{
		seq.push(s[len - 1]);
	}
	else if (s[len - 1] == ')' || s[len - 1] == ']')
	{
		if (seq.size() == 0) { return; }
		else if ((seq.top() == '(' && s[len - 1] == ')') || (seq.top() == '[' && s[len - 1] == ']'))
		{
			seq.pop();
		}
		else { return; }
	}
	//if (n == 0 || seq.size() > n - len) { return; }
	if (len == n)
	{
		if (seq.size() == 0)
		{
			std::cout << s << "\n";
			return;
		}
	}
	generate(s + "(", n, len + 1, seq);
	generate(s + "[", n, len + 1, seq);
	generate(s + ")", n, len + 1, seq);
	generate(s + "]", n, len + 1, seq);
	return;
}
int main()
{
	int n = 0;
	std::cin >> n;
	if (n % 2 == 1)
	{
		std::cout << "";
	}
	else
	{
		std::stack<char> seq;
		generate("(", n, 1, seq);
		generate("[", n, 1, seq);
	}
	return 0;
}