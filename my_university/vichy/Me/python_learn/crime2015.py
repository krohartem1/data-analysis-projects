import csv
import re

d = {}
with open("C:\\Users\\79125\\Downloads\\Crimes.csv") as f:
    file = csv.reader(f)
    for line in file:
        if re.search("2015", line[2]):
            if line[5] in d:
                d[line[5]] += 1
            else:
                d[line[5]] = 1
max = -1
ans = ""
for key in d:
    if d[key] > max:
        max = d[key]
        ans = key
print(ans)
