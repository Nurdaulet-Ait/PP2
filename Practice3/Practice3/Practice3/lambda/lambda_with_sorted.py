cars = [
    {"car": "Ford", "year": 2005},
    {"car": "BMW", "year": 2019},
    {"car": "Volvo", "year": 2011}
]

cars.sort(key=lambda x: x["year"])

print(cars)
