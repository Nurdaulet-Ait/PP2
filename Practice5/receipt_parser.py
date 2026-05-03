import re

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("--- Products and Prices ---")
item_pattern = r"(?P<item>.*?)\n(?P<count>[\d,]+)\s+x\s+(?P<price>[\d\s,]+)\n(?P<total>[\d\s,]+)"
matches = re.finditer(item_pattern, text)

for match in matches:
    print(f"{match.group('item').strip()}: {match.group('price').strip()}")

print("\n--- Total ---")
total_pattern = r"ИТОГО:\n(?P<total>[\d\s,]+)"
total_match = re.search(total_pattern, text)
print(total_match.group("total").strip() if total_match else "Not found")

print("\n--- Date and Time ---")
time_pattern = r"Время:\s+(?P<time>[\d\.:\s]+)"
time_match = re.search(time_pattern, text)
print(time_match.group("time").strip() if time_match else "Not found")

print("\n--- Address ---")
addr_pattern = r"г\.\s+.*"
addr_match = re.search(addr_pattern, text)
print(addr_match.group(0).strip() if addr_match else "Not found")


#ex 
import re

# 1
pattern = r"ab*"
print(bool(re.fullmatch(pattern, "abbb")))
print(bool(re.fullmatch(pattern, "a")))

# 2
pattern = r"ab{2,3}"
print(bool(re.fullmatch(pattern, "abb")))
print(bool(re.fullmatch(pattern, "abbb")))

# 3
text = "hello_world test_text example"
print(re.findall(r"[a-z]+_[a-z]+", text))

# 4
text = "Hello World Test Example"
print(re.findall(r"[A-Z][a-z]+", text))

# 5
pattern = r"a.*b"
print(bool(re.fullmatch(pattern, "a123b")))
print(bool(re.fullmatch(pattern, "ab")))

# 6
text = "Hello, world. Python is great"
print(re.sub(r"[ ,\.]", ":", text))

# 7
def snake_to_camel(s):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), s)

print(snake_to_camel("hello_world_test"))

# 8
text = "HelloWorldTest"
print(re.split(r"(?=[A-Z])", text))

# 9
text = "HelloWorldTest"
print(re.sub(r"(?<!^)(?=[A-Z])", " ", text))

# 10
def camel_to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()

print(camel_to_snake("HelloWorldTest"))