import requests
import re

A = input().replace("stepic.org", "stepik.org")
B = input().replace("stepic.org", "stepik.org")
t = False
res = requests.get(A)
for url1 in re.findall(r"href=[\"\'](.*)[\"\']>", res.text):
    res_2 = requests.get(url1)
    links = re.findall(
        r"href=[\"\'](.*)[\"\']", res_2.text.replace("stepic.org", "stepik.org")
    )
    if B in links:
        t = True
        print("Yes")
        break
if t == False:
    print("No")
