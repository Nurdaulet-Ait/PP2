import json

x = '{ "name": "Nurdaulet", "age": 20, "city": "Almaty" }'

y = json.loads(x)

print(y["name"])
print(y["age"])


student = {
    "name": "Nurdaulet",
    "age": 20,
    "city": "Almaty",
    "subjects": ["Python", "Math", "English"]
}

result = json.dumps(student)

print(result)


with open("student.json", "w") as file:
    json.dump(student, file)


with open("student.json", "r") as file:
    data = json.load(file)

print(data)


students = [
    {"name": "Ali", "age": 19},
    {"name": "Dana", "age": 20},
    {"name": "Aruzhan", "age": 18}
]

for student in students:
    print(student["name"])
