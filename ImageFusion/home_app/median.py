import numpy as np

def median_filter(c, n):
    m = np.zeros(c.shape)

    for i in range(0, c.shape[0]):
        for j in range(0, c.shape[1]):
            count = 0
            members = []
            for x in range(max(i - int(n/2), 0), min(i + int(n/2) + 1, c.shape[0])):
                for y in range(max(j - int(n/2), 0), min(j + int(n/2) + 1, c.shape[1])):
                    count =count + 1
                    members.append(c[i][j])
            np.sort(members)
            m[x][y] = members[int(count/2)]

    return m
