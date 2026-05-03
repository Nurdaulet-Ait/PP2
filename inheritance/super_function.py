class Person:
    def __init__(self, fname):
        self.firstname = fname

class Student(Person):
    def __init__(self, fname):
        super().__init__(fname)

x = Student("Nurdaulet")

print(x.firstname)
