def median_bucket(distribution, sum_left = 0, sum_right = 0):
    """Determine which bucket in the distribution contain the median."""
    # TODO implementati101, 121, 131, .... , 123, 99on
    head = 0
    tail = len(distribution) - 1
    sum_head = sum_left
    sum_tail = sum_right
    # sum_head = distribution[head]
    # sum_tail = distribution[tail]
    while (tail - head >= 0):
        current_min = min(sum_head, sum_tail)
        # print('The current min is {}'.format(current_min))
        if (current_min == sum_head):
            current_head_value = distribution[head]
            sum_head += current_head_value
            head = head + 1
        else:
            current_tail_value = distribution[tail]
            sum_tail += current_tail_value
            tail = tail - 1
        # print('The current sum head  is {} at {}'.format(sum_head, head))
        # print('The current sum tail is {} at {}'.format(sum_tail, tail))

    if (sum_head == sum_tail):
        return [head - 1, tail + 1]
    elif (sum_head > sum_tail):
        return [head - 1 ]
    else:
        return [tail + 1]
