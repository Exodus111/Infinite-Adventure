import random

r = random.Random()

ranseed = random.randint(1, 1000)
print ranseed

r.seed(795)

a = r.randint(1,5)
b = r.randint(1,5)

print a,b
