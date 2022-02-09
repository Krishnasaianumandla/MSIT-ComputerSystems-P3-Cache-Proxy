import time
from collections import OrderedDict

misses = {}
caches = {}


def caching(data, size_list):
    global caches, misses
    for size in size_list:
        if data not in caches[size]:
            misses[size] += 1
            caches[size][data] = data
            caches[size].move_to_end(data)
            if len(caches[size]) > int(size):
                caches[size].popitem(last=False)
        else:
            caches[size].move_to_end(data)
    pass


def accessDataRange(line, size_list):
    line = line.split(" ")
    b = int(line[1])
    y = int(line[2])
    n = int(line[3])
    for k in range(0, n):
        data = b + y * k
        caching(data, size_list)
    pass


def accessDataAddr(line, size_list):
    line = line.split(" ")
    data = int(line[1])
    caching(data, size_list)
    pass


def getStat(size_list):
    global misses
    stat_result = []
    for size in size_list:
        stat_result.append(misses[size])
        misses[size] = 0
    stat_result = str(stat_result).replace("[", "").replace("]", "").replace(", ", " ")
    print(stat_result)
    pass


def createCaches(size_list):
    global caches, misses
    for size in size_list:
        caches[size] = OrderedDict()
        misses[size] = 0
    pass


if __name__ == '__main__':
    start_time = time.time()

    num_caches = int(input())
    cache_capacity_list = input().split(" ")
    createCaches(cache_capacity_list)
    for input_line in iter(input, ""):
        if "RANGE" in input_line:
            accessDataRange(input_line, cache_capacity_list)
        elif "ADDR" in input_line:
            accessDataAddr(input_line, cache_capacity_list)
        elif "STAT" in input_line:
            getStat(cache_capacity_list)
        elif "END" in input_line:
            break

    time_elapsed = round(time.time() - start_time, 2)
    print(f"--- {time_elapsed} seconds ---")
