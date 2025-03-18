school = [[] for i in range(11)]
ans = [0 for i in range(11)]
with open("C:\\Users\\79125\\Downloads\\dataset_3380_5 (5).txt") as inf:
    for line in inf:
        work = line.split()
        school[int(work[0]) - 1].append(int(work[2]))
for i in range(11):
    sum = 0
    for x in school[i]:
        sum += x
    if len(school[i]) != 0:
        ans[i] = sum / len(school[i])
with open("C:\\Users\\79125\\Desktop\\test11.txt", "w") as ouf:
    for i in range(11):
        ouf.write(str(i + 1) + " ")
        if ans[i] == 0:
            ouf.write("-\n")
        else:
            ouf.write(str(ans[i]) + "\n")
