def median_bucket(distribution):
    """Determine which bucket in the distribution contain the median."""
    # TODO implementati101, 121, 131, .... , 123, 99on
    head = 0
    tail = len(distribution) - 1
    sum_head = distribution[head]
    sum_tail = distribution[tail]
    while (tail - head >= 2):
        print('The current sum head  is {}'.format(sum_head))
        print('The current sum tail is {}'.format(sum_tail))
        current_min = min(sum_head, sum_tail)
        print('The current min is {}'.format(current_min))
        if (current_min == sum_head):
            head = head + 1
            current_head_value = distribution[head]
            if(current_head_value == 0):
                alt_head = head -1
            sum_head += current_head_value
        else:
            tail = tail - 1
            current_tail_value = distribution[tail]
            # if (current_tail_value == 0):
            #     head = tail + 1
            sum_tail += current_tail_value

    max_result = max(sum_head, sum_tail)
    if (sum_head == sum_tail):
        return [head, tail]
    elif (max_result == sum_head):
        return [head]
    else:
        return [tail]
