#include <iostream>
#include <queue>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

bool check(string name)
{
    if (name[name.size() - 1] == 'b')
        return true;
    else
        return false;
}

string search(map<string, vector<string>> graph, string name)
{
    queue<string> search_queue;
    vector<string> proc;
    for (auto &x : graph[name])
    {
        search_queue.push(x);
    }

    while (!search_queue.empty())
    {
        string current = search_queue.front();
        search_queue.pop();
        if (find(proc.begin(), proc.end(), current) == proc.end())
        {
            if (check(current))
                return current;
            else
            {
                proc.push_back(current);
                for (auto &x : graph[current])
                {
                    search_queue.push(x);
                }
            }
        }
    }
    return "";
}

int main()
{
    map<string, vector<string>> graph;
    graph["alice"] = {"max", "adel", "vova"};
    graph["max"] = {"lika", "Sasha"};
    graph["Sasha"] = {"alice"};
    cout << search(graph, "alice");
}