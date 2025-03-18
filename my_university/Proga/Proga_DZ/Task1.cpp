#include <iostream>
#include <map>
int main()
{
    std::map<int, bool> subs;
    int x;
    while (std::cin >> x)
    {
        if (subs[x]) { std::cout << "YES\n"; }
        else { std::cout << "NO\n"; }
        subs[x] = 1;
    }
    return 0;
}