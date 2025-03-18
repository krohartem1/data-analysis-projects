from collections import deque

dict = {}
visited = []


def check(error):
    v = []
    list1 = deque()
    list1.append(error)
    while len(list1) != 0:
        if list1[0] in visited:
            return True
        if list1[0] not in v:
            v.append(list1[0])
            list1.extend(dict[list1[0]])
        list1.popleft()
    return False


n = int(input())
for i in range(n):
    s = input().split(":")
    child = (str(s[0]).split())[0]
    dict[child] = []
    if len(s) != 1:
        parents = str(s[1]).split()
        dict[child].extend(parents)
m = int(input())
for i in range(m):
    err = input()
    if check(err):
        print(err)
    visited.append(err)
