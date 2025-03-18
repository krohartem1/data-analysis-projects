#include <iostream>
#include <vector>

int bin_search(std::vector<int> m, int elem)
{
    if (m.empty())
        return -1;
    int begin = 0;
    int end = m.size() - 1;
    while (begin <= end)
    {
        int mid = (begin + end) / 2;
        if (m[mid] == elem)
            return mid;
        else if (m[mid] < elem)
            begin = mid + 1;
        else
            end = mid - 1;
    }
    return -1;
}

int main()
{
    std::vector<int> m = {-6, 1, 8, 9, 76};
    std::cout << bin_search(m, -6) + 1;
}