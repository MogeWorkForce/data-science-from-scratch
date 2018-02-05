# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import math
import random

from ..chapter_6.continuos_distribution import (
    normal_cdf, inverse_normal_cdf)


def normal_approximation_to_binomial(n, p):
    """finds mu and sigma corresponding to a Binomial(n, p)"""
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


# the normal cdf _is_ the probability the variable is below a threshold
normal_probability_below = normal_cdf


# it's above the threshold if it's not below the threshold
def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)


# it's between if it's less than hi, but not less than lo
def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


# it's outside if it's not between
def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


def normal_upper_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z <= z) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z >= z) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """returns the symmetric (about the mean) bounds
    that contain the specified probability"""
    tail_probability = (1 - probability) / 2

    # upper bound should have tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    # lower bound should have tail_probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound


def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # if x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail is what's less than x
        return 2 * normal_probability_below(x, mu, sigma)


def run_experiment():
    """flip a fair coin 1000 times, True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment):
    """using the 5% significance levels"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531


def estimated_parameters(N, n):
    """
        N = Space total of events
        n = occurrence of one type of event
    """
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma


def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)


if __name__ == "__main__":
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    # print(normal_two_sided_bounds(0.95, mu_0, sigma_0))

    # 95% bounds based on assumption p is 0.5
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    # actual mu and sigma based on p = 0.55
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
    # a type 2 error means we fail to reject the null hypothesis
    # which will happen when X is still in our original interval
    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    # print(power)

    hi = normal_upper_bound(0.95, mu_0, sigma_0)
    # print(hi)
    # is 526 (< 531, since we need more probability in the upper tail)
    type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    # print(power)

    # print(two_sided_p_value(529.5, mu_0, sigma_0))

    # extreme_value_count = 0
    # for _ in range(100000):
    #     num_heads = sum(1 if random.random() < 0.5 else 0
    #                     for _ in range(1000))
    #     if num_heads >= 530 or num_heads <= 470:
    #         extreme_value_count += 1
    #
    # print(extreme_value_count / 100000)
    # print(two_sided_p_value(531.5, mu_0, sigma_0))

    upper_p_value = normal_probability_above
    lower_p_value = normal_probability_below

    print(upper_p_value(524.5, mu_0, sigma_0))
    print(upper_p_value(526.5, mu_0, sigma_0))
    # print(lower_p_value)

    random.seed(0)
    experiments = [run_experiment() for _ in range(1000)]
    num_rejections = len([experiment
                          for experiment in experiments
                          if reject_fairness(experiment)])
    print(num_rejections)
