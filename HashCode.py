import numpy as np
import os
import sys, getopt

videos = np.empty(0)
endpoints = np.empty(0)
requests = np.empty(0)

cache_size = ""

NOT_CONNECTED = np.inf


def parse_input(filename):
    file = open(filename, 'r')
    line = file.readline()
    first_line = line.split()

    global endpoints
    global requests
    global videos

    endpoints = np.full((int(first_line[1]), int(first_line[3]) + 1), NOT_CONNECTED)

    requests = np.zeros((int(first_line[2]), 3))

    line = file.readline()
    secondLine = line.split()
    videos = np.array(secondLine).astype(np.int)

    for endpoint in range(int(first_line[1])):
        line = file.readline()
        line = line.split()
        endpoints[endpoint, int(first_line[3])] = line[0]

        for i in range(int(line[1])):
            line = file.readline()
            inner_line = line.split()
            endpoints[endpoint, int(inner_line[0])] = int(inner_line[1])

    for r in range(int(first_line[2])):
        line = file.readline()
        line = line.split()

        requests[r] = line






def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o", ["help=", "ifile=", "ofile"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('usage: HashCode.py -i input -o output')
            sys.exit()
        if opt in ("ifile", "-i"):
            parse_input(arg)

if __name__ == "__main__":
    main()