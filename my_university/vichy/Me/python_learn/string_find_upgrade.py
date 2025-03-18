s = input()
t = input()
ans = 0
for i in range(len(s)):
    if i + len(t) <= len(s) and s[i : i + len(t)] == t:
        ans += 1
print(ans)
