import math
import random

x = min(5, 10, 25)
y = max(5, 10, 25)

print(x)
print(y)


print(abs(-7.25))
print(round(5.76543, 2))
print(pow(4, 3))


print(math.sqrt(64))
print(math.ceil(1.4))
print(math.floor(1.4))


print(math.pi)
print(math.e)


print(math.sin(math.pi / 2))
print(math.cos(0))


print(random.random())
print(random.randint(1, 10))


fruits = ["apple", "banana", "cherry"]
print(random.choice(fruits))

random.shuffle(fruits)
print(fruits)



import math


#ex 

# 1
degree = 15
radian = degree * (math.pi / 180)
print(round(radian, 6))


# 2
height = 5
a = 5
b = 6

area = (a + b) * height / 2
print(area)


# 3
n = 4
side = 25

area = (n * side * side) / (4 * math.tan(math.pi / n))
print(round(area))


# 4
base = 5
height = 6

area = base * height
print(float(area))