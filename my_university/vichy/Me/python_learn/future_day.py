import datetime

str = input().split()
date = datetime.date(int(str[0]), int(str[1]), int(str[2]))
d = int(input())
date += datetime.timedelta(days=d)
print(date.year, date.month, date.day)
