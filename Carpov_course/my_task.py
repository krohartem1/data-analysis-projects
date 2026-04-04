from collections import Counter


def checkInclusion(s1, s2):
    counter_s1 = Counter(s1)
    s1_dict = dict(counter_s1)
    start = -1
    for cur in range(len(s2)):
        if s2[cur] not in s1_dict:
            if counter_s1 == Counter(s2[start + 1 : cur]):
                return True
            while start != cur:
                start += 1
                if s2[start] in s1_dict:
                    s1_dict[s2[start]] += 1
        else:
            s1_dict[s2[cur]] -= 1
            if s1_dict[s2[cur]] == 0:
                if counter_s1 == Counter(s2[start + 1 : cur + 1]):
                    return True
            if s1_dict[s2[cur]] < 0:
                if counter_s1 == Counter(s2[start + 1 : cur]):
                    return True
                while s2[start] != s2[cur]:
                    start += 1
                    if s2[start] in s1_dict:
                        s1_dict[s2[start]] += 1
    return False


print(checkInclusion("abc", "bbbca"))
