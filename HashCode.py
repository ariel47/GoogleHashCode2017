import numpy as np
import os
import sys, getopt

CAPACITY = ""

NOT_CONNECTED = np.inf

def algorithm(V, E, R):

    result = dict()

    for i in range(len(E[0]) - 1):
        # get the endpoints that are connected to the cache server
        E_inds = (E[:,i+1] < np.inf) # TODO: make sure this is the right condition
        E_inds = np.arange(E.shape[0])[E_inds]
        e = E[E_inds,:]
        print('E_inds', E_inds)
        print('e\n',e)

        # get the requests that come from these endpoints
        R_inds = np.in1d(R[:,1], E_inds)
        r = R[R_inds,:]
        if r.size == 0:
            continue
        print('R_inds', R_inds)
        print('r\n',r)

        # calculate the number of requests per video
        '''
        # use histogram with number of requests as weights
        # first fill with 0 for videos that have no requests
        scores, _ = np.histogram(r[:,0], bins=len(V), weights=r[:,2])
        scores = np.stack
        '''

        # unique_videos = np.unique(r[:,0])
        # print('unique videos', unique_videos)
        # r_per_video = np.zeros(unique_videos.size)
        # for j in unique_videos:
        #     r_j = (r[:,0] == j)
        #     print('r_j\n',r_j)
        #     print('r\n',r[r_j,2])
        #     r_per_video[j] = np.sum(r[r_j])
        # print('r_per_video', r_per_video)

        # fill the cache server with the most requested videos
        r_per_video = r
        order = np.argsort(r_per_video[:,2])[::-1]
        r_per_video = r_per_video[order,:]
        print('r_per_video\n',r_per_video)
        result_i = []
        capacity_i = 0
        for video in r_per_video[:,0]:
            if capacity_i + V[video] > CAPACITY:
                continue
            else:
                result_i.append(video)
                capacity_i += V[video]

        result[i] = result_i
        print('result_i', result_i)

    print('result\n', result)

    with open('result.txt', 'w') as f_out:
        f_out.write(str(len(result)) + '\n')
        for key, val in result.items():
            f_out.write(str(key) + ' ')
            for v in val:
                f_out.write(str(v) + ' ')
            f_out.write('\n')


def parse_input(filename):
    file = open(filename, 'r')
    line = file.readline()
    first_line = line.split()

    global CAPACITY
    CAPACITY = int(first_line[4])

    endpoints = np.full((int(first_line[1]), int(first_line[3]) + 1), NOT_CONNECTED)

    requests = np.zeros((int(first_line[2]), 3)).astype(np.int)

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

    return videos, endpoints, requests






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
            videos, endpoints, requests = parse_input(arg)
            algorithm(videos, endpoints, requests)

if __name__ == "__main__":
    main()