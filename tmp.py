a = 1
b = 2
c = 3
d = 4

cond = [
    a == 1,
    b == 2,
    c == 3,
    d == 4,
]
simple_cond = cond[0] and cond[1] and cond[2] and cond[3]
print("simple -------", simple_cond)
if simple_cond:
    age, race, curent_race = False, True, None
    cond.extend([curent_race is not None, age, race])
    print((not cond[4]) or (cond[5] and cond[6]))
else:
    print(simple_cond)
