namespace = {"global": ["None"]}
ans = []


def add(name, var):
    namespace[name].append(var)


def create(name, parent):
    namespace[name] = [parent]


def get(name, var):
    for i in range(1, len(namespace[name])):
        if namespace[name][i] == var:
            ans.append(name)
            return
    if name == "global":
        ans.append("None")
        return
    else:
        get(namespace[name][0], var)


n = int(input())
for i in range(n):
    str = input().split()
    if str[0] == "add":
        add(str[1], str[2])
    elif str[0] == "create":
        create(str[1], str[2])
    else:
        get(str[1], str[2])
for x in ans:
    print(x)
