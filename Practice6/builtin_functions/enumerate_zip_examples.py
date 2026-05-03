names = ["Ali", "Dana", "Aruzhan"]
scores = [90, 85, 88]

for i, name in enumerate(names):
    print(i, name)

for name, score in zip(names, scores):
    print(name, score)
