class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name

p1 = Person("Ali")
p2 = Person("Dana")

print(p1.species)
print(p2.species)
