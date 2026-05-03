class Person:
    def __init__(self, name):
        self.name = name

    def myfunc(self):
        print("Hello my name is " + self.name)

p1 = Person("Nurdaulet")
p1.myfunc()
