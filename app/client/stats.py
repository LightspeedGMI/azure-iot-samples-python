import sys
import math

def get_max_min(readfile):
    # not used
    min = -1
    max = -1
    with open(readfile, 'rU') as f:
        for line in f:
            try:
                number=int(line.strip())
                if min != -1 and max != -1:
                    if number < min:
                        min = number
                    if number > max:
                        max = number
                else:
                    min = number
                    max = number
            except Exception:
                pass
        return {max, min}


def less_than(readfile, target):
    # not used
    count = 0
    with open(readfile, 'rU') as f:
        for line in f:
            try:
                number=int(line.strip())
                if number < target:
                    count = count + 1
            except Exception:
                pass
        return count

def get_dist(lines, min_range, max_range, buckets):
    # calculate the bucket "step"
    step = int(math.floor((max_range - min_range) / buckets))

    # initialize the counts
    counts = []
    for i in range(buckets):
        counts.append(0)

    for line in lines:
        try:
            number=int(line.strip())
            bucket_number = number / step
            counts[bucket_number] = counts[bucket_number] + 1
        except Exception:
            pass
    return counts


def get_dist_file(file_name, min_range, max_range, buckets):
    # iterate the file once to get the counts
    with open(readfile, 'rU') as f:
        return get_dist(f, min_range, max_range, buckets)

#args = sys.argv
#readfile = args[1]
#min_range = int(args[2])
#max_range = int(args[3])
#buckets = int(args[4])

#dist_list = get_dist(min_range, max_range, buckets)

#print(dist_list)
#print(sum(dist_list))
