def primes():
    lst = [2]
    yield 2
    i = 2
    while True:
        i += 1
        if (i > 10) and (i % 10 == 5):
            continue
        for j in lst:
            if j * j - 1 > i:
                yield i
                lst.append(i)
                break
            if i % j == 0:
                break
        else:
            yield i
            lst.append(i)
