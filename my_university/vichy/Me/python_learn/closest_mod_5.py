def closest_mod_5(x):
    a = [0, 1, 2, 3, 4]
    for k in a:
        if (x + k) % 5 == 0:
            return x + k
