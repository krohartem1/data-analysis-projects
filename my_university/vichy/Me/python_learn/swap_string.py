s = input()
a = input()
b = input()
ans = 0
while s.find(a) != -1:
    if ans > 1000:
        break
    ans += 1
    s = s.replace(a, b)
if ans > 1000:
    print("Impossible")
else:
    print(ans)
