# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

from matplotlib import pyplot as plt


def average(interval, func):
    return (
               func(interval[1]) - func(interval[0])
           ) / (interval[1] - interval[0])


if __name__ == "__main__":
    fn = lambda x: 64 - 16 * (x - 1) ** 2

    """
        Construct an accurate graph of y = s(t) on the time interval 0 ≤ t ≤ 3. Label at
        least six distinct points on the graph, including the three points that correspond
        to when the ball was released, when the ball reaches its highest point, and when
        the ball lands.
    """
    response_a = [fn(item / 2) for item in range(0, 7) if item / 2 <= 3]

    points = [item / 2 for item in range(0, 7) if item / 2 <= 3]
    gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]

    response_c = average([0.5, 1], fn)

    print(response_c)
    # # create a line chart, years on x-axis, gdp on y-axis
    # plt.plot(points, response_a, color='green', marker='o', linestyle='solid')
    # # add a title
    # plt.title("Velocity")
    # # add a label to the y-axis
    # plt.ylabel("Feets")
    # plt.xlabel("Time (seconds)")
    # plt.show()

    points_to_calculate = [
        [0.4, 0.8], [0.7, 0.8], [0.79, 0.8], [0.799, 0.8], [0.8, 1.2],
        [0.8, 0.9], [0.8, 0.81], [0.8, 0.801]
    ]

    average_calculated = [
        average(interval, fn) for interval in points_to_calculate
    ]
    print(average_calculated)

    print(average([1.5, 2], fn))
    print(fn(1.5), fn(2), fn(1), fn(0.5))
