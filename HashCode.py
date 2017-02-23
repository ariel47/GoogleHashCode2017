import numpy as np
import os
import sys, getopt
import time

CAPACITY = ""

NOT_CONNECTED = np.inf

def algorithm(V, E, R, filename):

    result = dict()

    E = E[:,-1].reshape(-1,1) - E
    E[E < 0] = 0
    
    for i in range(len(E[0]) - 1):
        # get the endpoints that are connected to the cache server
        E_inds = (E[:,i] < np.inf) # TODO: make sure this is the right condition
        E_inds = np.arange(E.shape[0])[E_inds]
        endpoints = E[E_inds,:]

        # get the requests that come from these endpoints
        R_inds = np.in1d(R[:,1], E_inds)
        requests = R[R_inds,:]
        if requests.size == 0:
            continue

        # calculate the score - R_N * (L_D -L)
        latency = endpoints[requests[:,1], i]
        requests[:,2] = requests[:,2] * latency
        
        # calculate the number of requests per video
        '''
        # use histogram with number of requests as weights
        # first fill with 0 for videos that have no requests
        scores, _ = np.histogram(r[:,0], bins=len(V), weights=r[:,2])
        scores = np.stack
        '''

        unique_videos = np.unique(requests[:,0])
        unique_videos = np.random.choice(unique_videos, min(130, unique_videos.size), replace=False)

        r_per_video = np.zeros(V.size, dtype=np.int64)
        for j in unique_videos:
            r_j = (requests[:,0] == j)
            r_per_video[j] = np.sum(requests[r_j, 2])

        # fill the cache server with the most requested videos
        np.true_divide(r_per_video, V) # divide by size
        r_per_video = np.vstack([np.arange(V.size), r_per_video]).T
        order = np.argsort(r_per_video[:,1])[::-1]
        r_per_video = r_per_video[order,:]
        result_i = []
        capacity_i = 0
        for video in r_per_video[:,0]:
            if capacity_i + V[video] > CAPACITY:
                continue
            else:
                result_i.append(video)
                capacity_i += V[video]

        result[i] = result_i

    with open(filename + '.txt', 'w') as f_out:
        f_out.write(str(len(result)) + '\n')
        for key, val in result.items():
            f_out.write(str(int(key)) + ' ')
            for v in val:
                f_out.write(str(int(v)) + ' ')
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
    start = time.time()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o", ["help=", "ifile=", "ofile"])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            #print('usage: HashCode.py -i input -o output')
            sys.exit()
        if opt in ("ifile", "-i"):
            videos, endpoints, requests = parse_input(arg)
            algorithm(videos, endpoints, requests, arg)

    print('time: {:.2f}'.format(time.time() - start))


if __name__ == "__main__":
    main()