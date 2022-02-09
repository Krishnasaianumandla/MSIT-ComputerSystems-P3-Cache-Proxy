# result.write(str("data") + "\n")
# result.close()
import random

result = open("input.txt", "w")


def getRange():
    x = random.randint(0, 20000)
    y = random.randint(1, 20000)
    z = random.randint(1, 20000)
    output = f"RANGE {x} {y} {z}\n"
    return output


def getAddr():
    y = random.randint(1, 20000)
    output = f"ADDR {y}\n"
    return output


data = random.randint(1, 30)
# data = 30
result.write(str(data) + "\n")

cache_size = []

for i in range(data):
    size = random.randint(2, pow(2, 20))
    cache_size.append(size)
data = str(cache_size).replace("[", "").replace("]", "").replace(", ", " ")
result.write(str(data) + "\n")

num_lines = random.randint(0, 20000)

data = ""
for i in range(num_lines):
    rand_val = random.randint(1, 3)
    if rand_val == 1:
        data = getRange()
        result.write(str(data))
    elif rand_val == 2:
        data = getAddr()
        result.write(str(data))
    else:
        data = "STAT\n"
        result.write(str(data))

data = "END"
result.write(str(data))
