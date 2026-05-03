def my_function(*args):
    print(args[0])

my_function("Ali", "Dana", "Aruzhan")


def my_function(**kwargs):
    print(kwargs["name"])

my_function(name="Nurdaulet", age=20)
