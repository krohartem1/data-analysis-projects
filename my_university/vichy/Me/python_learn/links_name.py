import requests
import re

url = input()
res = requests.get(url)
ans = []
links = re.findall(r"<a.*href=[\'\"]([^\'\"\?:/]*)://(\w[^\'\"\?:/]*)(.*)>", res.text)
for link in links:
    if link[1] not in ans:
        ans.append(link[1])
ans.sort()
for x in ans:
    print(x)
