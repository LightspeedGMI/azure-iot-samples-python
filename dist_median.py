import fileinput
import shutil

N = 1000000


# runs on PI
def median_counts(device_seq, median, keep_values):
    with open('vibrations-m%d.txt' % device_seq, 'r') as f:
        low, high, eq = 0, 0, 0
        for line in f.readlines():
            if not line.startswith('vibration'):
                n = int(line)
                if n < median:
                    low += 1
                if n > median:
                    high += 1
                if n == median:
                    eq += 1
    # TODO cache count of numbers under and over the keep_values window
    # TODO discard numbers outside the keep_values window from the file to speed up next iteration
    return low, eq, high


def accumulate_counts(device_ids, median, keep_values):
    lows, eqs, highs = 0, 0, 0
    for device_id in device_ids:
        low, eq, high = median_counts(device_id, median, keep_values)
        lows += low
        highs += high
        eqs += eq
    return lows, highs, eqs


state = {
    "low_median": 0,
    "high_median": N,
    "approx_median": None,
    "low_low_count": 0,
    "high_high_count": 0
}

num_devices = 6
low_median = 305525
high_median = 305529

# 4 dataset
num_devices = 4
low_median = 262682
high_median = 262686

num_devices = 6
low_median = 0
high_median = N


while True:
    approx_median = (low_median + high_median) / 2

    lcount, hcount, ecount = accumulate_counts(range(0, num_devices), approx_median, (low_median, high_median))

    print(low_median, lcount, approx_median, ecount, hcount, high_median)

    if lcount < hcount:
        low_median = approx_median
    elif hcount < lcount:
        high_median = approx_median

    print("Median: " + str(approx_median))

    if approx_median == (low_median + high_median) / 2:
        if (ecount == 0) and ((lcount + hcount) % 2 == 0):
            print("Median %f: " % (low_median + high_median) / 2.0)
        else:
            print("Median %d: " % approx_median)
        break
