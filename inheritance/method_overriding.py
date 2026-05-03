class Animal:
    def sound(self):
        print("Sound")

class Dog(Animal):
    def sound(self):
        print("Bark")

d = Dog()
d.sound()
