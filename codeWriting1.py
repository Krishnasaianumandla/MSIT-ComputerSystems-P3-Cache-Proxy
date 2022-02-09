class Cache:
    def __init__(self, capacity):
        self.size = capacity
        self.cache_list = []
        self.miss = 0

    def check(self, data):
        if data in self.cache_list:
            self.cache_list.remove(data)
            self.cache_list.append(data)
        else:
            self.miss += 1
            self.cache_list.append(data)
            if len(self.cache_list) > self.size:
                self.cache_list.pop(0)
        pass

    def getMiss(self):
        return self.miss

    def resetMiss(self):
        self.miss = 0
        pass


def addDataReference(data, caches):
    for cache in caches:
        cache.check(data)
    pass


def processRange(line, caches):
    line = line.split(" ")
    b = int(line[1])
    y = int(line[2])
    n = int(line[3])
    for k in range(0, n):
        data = b + (y * k)
        addDataReference(data, caches)
    pass


def processAddr(line, caches):
    line = line.split(" ")
    data = int(line[1])
    addDataReference(data, caches)
    pass


def processStat(caches):
    misses = []
    for cache in caches:
        misses.append(cache.getMiss())
        cache.resetMiss()

    misses = str(misses).replace("[", "").replace("]", "").replace(", ", " ")
    print(misses)
    pass


if __name__ == '__main__':
    num_caches = int(input())
    cache_capacity_list = input().split(" ")

    caches_list = []
    for size in cache_capacity_list:
        caches_list.append(Cache(int(size)))

    for input_line in iter(input, ""):
        if "RANGE" in input_line:
            processRange(input_line, caches_list)
        elif "ADDR" in input_line:
            processAddr(input_line, caches_list)
        elif "STAT" in input_line:
            processStat(caches_list)
        elif "END" in input_line:
            break
