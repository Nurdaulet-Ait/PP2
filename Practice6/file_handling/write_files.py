with open("test.txt", "w") as f:
    f.write("Hello\n")
    f.write("Python\n")

with open("test.txt", "a") as f:
    f.write("Append line\n")
