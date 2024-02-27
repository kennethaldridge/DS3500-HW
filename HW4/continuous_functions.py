"""
File: continuous_functions.py
Description: Functions that approximate the continuous distribution
to a discrete distribution
"""
from collections import defaultdict
import numpy as np


def uni_dist(a, b, bins):
    """Approximates the uniform distribution
    :param a: Starting point
    :param b: Ending point
    :param bins: Number of bins to approximate the distribution with
    :return dist: approximated discrete distribution"""

    dist = defaultdict()
    prob = 1 / (b - a)   # the probability for each point

    values = np.linspace(a, b, bins)   # generate evenly spaced bins

    for val in values:
        dist[val] = prob

    return dist


def norm_dist(mean, sd, bin_count, val_count):
    """Approximates the normal distribution
    :param mean: The mean of the normal distribution
    :param sd: The standard deviation of the normal distribution
    :param bin_count: The number of bins to approximate the distribution with
    :param val_count: The number of points to generate for the normal distribution
    :return dist: approximated discrete distribution"""

    vals = [np.random.normal(mean, sd) for _ in range(val_count)]  # generate the points on the normal distribution

    # get the max and the min values and then generate evenly spaced bins
    minv = min(vals)
    maxv = max(vals)
    bins = np.linspace(minv, maxv, bin_count)

    dist = defaultdict(lambda: 0)  # initialize dictionary with default value of 0
    for val in vals:
        # count the number of values in each bin
        bin = min(bins, key=lambda x: abs(x - val))
        dist[bin] += 1

    # get the probability of each bin by dividing the count by the total
    dist = {key: dist[key] / sum(dist.values()) for key in dist.keys()}

    return dist
