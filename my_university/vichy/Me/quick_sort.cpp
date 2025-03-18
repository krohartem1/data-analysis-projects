#include <iostream>
#include <vector>
std::vector<int> quicksort(std::vector<int> &arr)
{
    if (arr.size() < 2)
        return arr;
    int pivot = arr[arr.size() / 2];
    std::vector<int> left;
    std::vector<int> right;
    std::vector<int> mid;
    for (int i = 0; i < arr.size(); ++i)
    {
        if (arr[i] < pivot)
        {
            left.push_back(arr[i]);
        }
        else if (arr[i] > pivot)
        {
            right.push_back(arr[i]);
        }
        else
        {
            mid.push_back(pivot);
        }
    }
    std::vector<int> all;
    for (auto x : quicksort(left))
    {
        all.push_back(x);
    }
    for (int i = 0; i < mid.size(); ++i)
    {
        all.push_back(pivot);
    }
    for (auto x : quicksort(right))
    {
        all.push_back(x);
    }
    return all;
}

int main()
{
    std::vector<int> arr = {-5, 545, -20, 15, 48, 125, 326, 48, -48, 98, -8858};
    for (auto x : quicksort(arr))
    {
        std::cout << x << " ";
    }
    return 0;
}