# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import math
import random

from collections import Counter

from matplotlib import pyplot as plt
from ..chapter_4.vectors import shape, get_column, make_matrix
from ..chapter_5.stats_formula import mean, standard_deviation, correlation
from ..chapter_6.continuos_distribution import inverse_normal_cdf


def bucketize(point, bucket_size):
    """floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)


def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()


def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())


def correlation_matrix(data):
    """returns the num_columns x num_columns matrix whose (i, j)th entry
    is the correlation between columns i and j of data"""
    _, num_columns = shape(data)

    def matrix_entry(i, j):
        return correlation(get_column(data, i), get_column(data, j))

    return make_matrix(num_columns, num_columns, matrix_entry)


if __name__ == "__main__":
    random.seed(0)
    # uniform between -100 and 100
    uniform = [200 * random.random() - 100 for _ in range(10000)]
    # normal distribution with mean 0, standard deviation 57
    normal = [57 * inverse_normal_cdf(random.random())
              for _ in range(10000)]

    print(mean(uniform), mean(normal))
    print(standard_deviation(uniform), standard_deviation(normal))
    # plot_histogram(uniform, 10, "Uniform Histogram")
    #
    # plot_histogram(normal, 10, "Normal Histogram")

    xs = [random_normal() for _ in range(1000)]
    ys1 = [x + random_normal() / 2 for x in xs]
    ys2 = [-x + random_normal() / 2 for x in xs]

    print(mean(ys1), mean(ys2))
    print(standard_deviation(ys1), standard_deviation(ys2))
    print(correlation(xs, ys1), correlation(xs, ys2))
    plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
    plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    plt.title("Very Different Joint Distributions")
    plt.show()

    # commented because we don't have now some data_set to test these
    # code bellow
    # data = []
    # _, num_columns = shape(data)
    # fig, ax = plt.subplots(num_columns, num_columns)
    # for i in range(num_columns):
    #     for j in range(num_columns):
    # # scatter column_j on the x-axis vs column_i on the y-axis
    # if i != j:
    #     ax[i][j].scatter(get_column(data, j), get_column(data, i))
    # # unless i == j, in which case show the series name
    # else:
    #     ax[i][j].annotate("series " + str(i), (0.5, 0.5),
    #                       xycoords='axes fraction',
    #                       ha="center", va="center")
    # # then hide axis labels except left and bottom charts
    # if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
    # if j > 0: ax[i][j].yaxis.set_visible(False)
    # # fix the bottom right and top left axis labels, which are wrong because
    # # their charts only have text in them
    # ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
    # ax[0][0].set_ylim(ax[0][1].get_ylim())
    # plt.show()
