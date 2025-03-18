#include <iostream>
#include <queue>
#include <map>
#include <vector>
#include <string>
#include <algorithm>
#include <utility>
#include <limits>

using namespace std;

auto find_lowest_node(map<string, pair<int, bool>> &costs)
{
    int lowest_node_cost = std::numeric_limits<int>::max();
    string lowest_node = "";
    for (auto &x : costs)
    {
        if (!x.second.second)
        {
            if (x.second.first < lowest_node_cost)
            {
                lowest_node_cost = x.second.first;
                lowest_node = x.first;
            }
        }
    }
    return lowest_node;
}

map<string, string> Djiikstra(map<string, vector<pair<string, int>>> &graph, map<string, pair<int, bool>> costs, string start)
{
    vector<string> processed = {};
    map<string, string> parents;
    parents[start] = "";
    costs[start] = {0, 0};

    string node = find_lowest_node(costs);
    while (node != "")
    {
        for (auto &x : graph[node])
        {
            int cost = costs[node].first + x.second;
            if (cost < costs[x.first].first)
            {
                costs[x.first].first = cost;
                parents[x.first] = node;
            }
        }
        costs[node].second = 1;
        node = find_lowest_node(costs);
    }

    return parents;
}

int main()
{

    return 0;
}