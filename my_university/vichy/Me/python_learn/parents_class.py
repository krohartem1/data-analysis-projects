from collections import deque

dict = {}


def parents_class(par, child):
    if par not in dict or child not in dict:
        return False
    list1 = deque()
    list1.append(child)
    visited = []
    while len(list1) != 0:
        if list1[0] == par:
            return True
        if list1[0] not in visited:
            visited.append(list1[0])
            list1.extend(dict[list1[0]])
        list1.popleft()
    return False


n = int(input())
for i in range(n):
    s = input().split(":")
    child = (str(s[0]).split())[0]
    dict[child] = [child]
    if len(s) != 1:
        parents = str(s[1]).split()
        dict[child].extend(parents)
q = int(input())
for i in range(q):
    str = input().split()
    if parents_class(str[0], str[1]) == True:
        print("Yes")
    else:
        print("No")
