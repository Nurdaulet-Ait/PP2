mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        x = self.a
        self.a += 1
        return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))


def my_generator():
    yield 1
    yield 2
    yield 3

for x in my_generator():
    print(x)


numbers = (x * x for x in range(5))

for x in numbers:
    print(x)

#ex

# 1
def squares_up_to(n):
    for i in range(n + 1):
        yield i * i

for x in squares_up_to(5):
    print(x)


# 2
n = int(input())

def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print(",".join(str(x) for x in even_numbers(n)))


# 3
def divisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for x in divisible(50):
    print(x)


# 4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

for x in squares(2, 6):
    print(x)


# 5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

for x in countdown(5):
    print(x)