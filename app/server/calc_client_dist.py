import sys

def calc_client_dist():
    dists=[]
    dists.append([[1,2], [1,2,3]])
    dists.append([[2], [4,5,6]])
    dists.append([[2], [7,8,9]])

    # initialize accumulative result
    accum_list = []
    for i in range(len(dists[0][1])):
        accum_list.append(0)

    # "collapse" multiple dist lists into result
    for dist in dists:
        accum_list = map(sum, zip(accum_list, dist[1]))

    return accum_list

print(calc_client_dist())
