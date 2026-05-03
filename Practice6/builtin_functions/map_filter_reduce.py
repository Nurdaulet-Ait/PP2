from functools import reduce

numbers = [1, 2, 3, 4, 5]

mapped = list(map(lambda x: x * 2, numbers))
print(mapped)

filtered = list(filter(lambda x: x % 2 == 0, numbers))
print(filtered)

reduced = reduce(lambda x, y: x + y, numbers)
print(reduced)
