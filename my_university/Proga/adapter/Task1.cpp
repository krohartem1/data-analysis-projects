/*#include<iostream>
#include <stack>
#include <string>
int main()
{
	std::string s;
	std::cin >> s;
	std::stack<char> seq;
	seq.push(' ');
	for (size_t i = 0; i < s.size(); ++i)
	{
		if (seq.top() != ')' || seq.top() != '}' || seq.top() != ']')
		{
			if ((seq.top() == '(' && s[i] == ')') || (seq.top() == '{' && s[i] == '}') || (seq.top() == '[' && s[i] == ']'))
			{
				seq.pop();
			}
			else {
				seq.push(s[i]);
			}
		}
		else { break; }
	}
	if (seq.top() == ' ') { std::cout << "YES"; }
	else { std::cout << "NO"; }
	return 0;
}*/