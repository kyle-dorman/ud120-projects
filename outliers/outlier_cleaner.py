#!/usr/bin/python

import math

def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """

    cleaned_data = []

    ### your code goes here

    if len(predictions) != len(ages) or len(ages) != len(net_worths):
        print "Invalid length of an input array"
        return cleaned_data

    cleaned_data = [(ages[i], net_worths[i], r_squared(predictions[i], net_worths[i])) for i in xrange(len(ages))]
    cleaned_data = sorted(cleaned_data, key= lambda item: item[2])

    last = int(math.ceil(len(cleaned_data) / 10.)) * 9

    return cleaned_data[0:last]

def r_squared(estimated, actual):
    return (estimated - actual)**2

