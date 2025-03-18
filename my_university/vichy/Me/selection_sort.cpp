#include <iostream>
#include <vector>

int smallest_index(std::vector<int> &a)
{
    int small_elem = a[0];
    int small_ind = 0;
    for (int i = 0; i < a.size(); ++i)
    {
        if (a[i] < small_elem)
        {
            small_elem = a[i];
            small_ind = i;
        }
    }
    return small_ind;
}

void selection_sort(std::vector<int> &a)
{
    if (a.empty())
        return;
    std::vector<int> arr(a.size());
    int n = a.size();
    for (int i = 0; i < n; ++i)
    {
        int ind = smallest_index(a);
        arr[i] = a[ind];
        a.erase(a.begin() + ind);
    }
    a = arr;
}

int main()
{
    std::vector<int> a = {1, 1, 1, 5, 5, 8, 4, 9};
    selection_sort(a);
    for (auto &x : a)
        std::cout << x << " ";
    return 0;
}