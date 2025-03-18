#include <vector>
#include <string>
#include <array>
#include <deque>
#include <list>
#include <forward_list>
#include <iostream>
#include <iterator>
template <typename Conteiner>
void Print(Conteiner& a, std::string s)
{
    auto iterator = a.begin();
    std::cout << *iterator;
    ++iterator;
    for (auto iter = iterator; iter != a.end(); ++iter)
    {
        std::cout << s << *iter;
    }
}

int main()
{
    std::vector<int> data = { 1, 2, 3, 4 };
    Print(data, ", ");  // 1, 2, 3, 4
    return 0;
}