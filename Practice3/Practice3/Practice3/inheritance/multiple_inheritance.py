class Father:
    def drive(self):
        print("Driving")

class Mother:
    def cook(self):
        print("Cooking")

class Child(Father, Mother):
    pass

c = Child()

c.drive()
c.cook()
