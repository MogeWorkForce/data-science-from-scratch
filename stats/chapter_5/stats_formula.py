# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import math
import random
from collections import Counter

from ..chapter_4.vectors import sum_of_squares


def mean(items):
    return sum(items) / len(items)


def median(items):
    items_sorted = sorted(items)
    n = len(items)
    midpoint = n // 2

    if n % 2 == 1:
        # if odd return middle value
        return items_sorted[midpoint]

    # if even return mean of middle values
    middle_left = midpoint - 1
    middle_right = midpoint

    return (middle_left + middle_right) / 2


def quantile(items, percentile):
    """returns the pth-percentile value in x"""
    p_index = int(percentile * len(items))
    return sorted(items)[p_index]


def mode(items):
    counts = Counter(items)
    max_count = max(counts.values())
    return [
        x_i for x_i, count in counts.items()
        if count == max_count
    ]


def data_range(items):
    return max(items) - min(items)


def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)


def standard_deviation(x):
    return math.sqrt(variance(x))


def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)
