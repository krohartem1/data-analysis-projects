/*
#include <vector>
#include <algorithm>
#include <iostream>
template <typename T>
void Duplicate(std::vector<T>& v) {
    std::vector<T>v_0;
    v_0.resize(v.size());
    std::copy(v.begin(), v.end(), v_0.begin());
    for (auto it = v.begin(); it != v.end(); ++it) {
        v_0.push_back(*it);
    }
    v.clear();
    v.resize(v_0.size());
    std::copy(v_0.begin(), v_0.end(), v.begin());
    v_0.clear();
}

int main()
{
    std::vector<int>v;
    v.push_back(5);
    v.push_back(4);
    v.push_back(3);
    v.push_back(2);
    v.push_back(1);
    Duplicate(v);
    for (const auto& x : v)
    {
        std::cout << x << " ";
    }
    return 0;
}*/