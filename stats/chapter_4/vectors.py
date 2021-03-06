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


def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_rows, num_cols


def get_row(A, i):
    return A[i]  # A[i] is already the ith row


def get_column(A, j):
    return [A_i[j]
            for A_i in A]


def make_matrix(num_rows, num_cols, entry_fn):
    #make_matrix(n1, k2, partial(matrix_product_entry, A, B))
    """returns a num_rows x num_cols matrix
    whose (i,j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j)  # given i, create a list
             for j in range(num_cols)]  # [entry_fn(i, 0), ...]
            for i in range(num_rows)]  # create one list for each i


def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0


identity_matrix = make_matrix(5, 5, is_diagonal)
