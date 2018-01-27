# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import math
from functools import partial, reduce


def vector_add(v, w):
    return [v_i + w_i
            for v_i, w_i in zip(v, w)]


def vector_subtract(v, w):
    return [v_i - w_i
            for v_i, w_i in zip(v, w)]


vector_sum = partial(reduce, vector_add)


def scalar_multiply(scalar, vector):
    """c is a number, v is a vector"""
    return [scalar * v_i for v_i in vector]


def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the
    ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1 / n, vector_sum(vectors))


def dot(v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
               for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * v_n"""
    return dot(v, v)


def magnitude(v):
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    return magnitude(vector_subtract(v, w))