#!/usr/home/bordo/chess-compression-analytics/bin/python3.8

import matplotlib.pyplot as plt
import numpy
import numpy as np

pltpoints = 30
with open("lichess_res.txt", "r") as lichess_res:
    x = lichess_res.read().split("\n")
    x.pop(-1)
    print(x)
    y = []
    for item in x: y.append(int(item))

    tot = sum(y)

    freq = list(map(lambda x: x/tot, y))
    index = list(range(len(freq)))
    for i in range(8):
        print(index[i], freq[i])
    plt.plot(index[:pltpoints], freq[:pltpoints])


with open("./rust_test_stripped.csv", "r") as res:

    x = res.read().split(",")
    x.pop(-1)
    y = []
    for item in x:
        y.append(int(item))

    y = np.array(y)
    # plt.hist(y,bins=np.arange(y.min(), y.max()+1))
    # plt.show()

    print(list(map(int, x)))
    print("Data skew: " + str(3 * (numpy.average(y) - numpy.median(y)) / numpy.std(y)))
    index, counts = numpy.unique(y, return_counts=True)
    print(len(index), len(counts))
    freq = []
    for i in range(len(counts)):
        freq.append(counts[i] / float(len(y)))
    for i in range(8):
        print(index[i], freq[i])

    plt.plot(index[:pltpoints], freq[:pltpoints])

with open("./modern35.csv", "r") as res:

    x = res.read().split(",")
    x.pop(-1)
    y = []
    for item in x:
        y.append(int(item))

    y = np.array(y)
    # plt.hist(y,bins=np.arange(y.min(), y.max()+1))
    # plt.show()

    print(list(map(int, x)))
    print("Data skew: " + str(3 * (numpy.average(y) - numpy.median(y)) / numpy.std(y)))
    index, counts = numpy.unique(y, return_counts=True)
    print(len(index), len(counts))
    freq = []
    for i in range(len(counts)):
        freq.append(counts[i] / float(len(y)))
    for i in range(8):
        print(index[i], freq[i])

    plt.plot(index[:pltpoints], freq[:pltpoints])
plt.show()
plt.savefig("lc_vs_rust_vs__py_mod35.png")