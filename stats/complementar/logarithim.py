# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

from collections import defaultdict


def is_valid_factorial(value, used):
    for x in used:
        if value % x == 0:
            return False
    return True


class Factorize:
    original_value = 1

    def calculate_factorial(self, original_value):
        negative = False
        if original_value < 0:
            negative = True
        elif original_value == 0:
            raise Exception("Cannot possible calculate factorial of 0")
        elif original_value == 1:
            return original_value, {1: 1}

        used = [2]
        self.original_value = original_value
        current_value = abs(original_value)

        dict_factorial = defaultdict(int)
        current_factorial = 2
        while current_value != 1:
            if current_value % current_factorial == 0:
                current_value = current_value / current_factorial
                dict_factorial[current_factorial] += 1
            else:
                valid = False
                while not valid:
                    current_factorial += 1
                    if is_valid_factorial(current_factorial, used):
                        used.append(current_factorial)
                        valid = True

        if negative:
            dict_factorial[-1] = 1

        return self.original_value, dict_factorial


class LogarithimError(Exception):
    pass


class Logarithim:
    base = None

    def __init__(self, base=None, logarithimand=None, total=None,
                 force_calculate_base=False):

        self.base = base
        self.logarithimand = logarithimand
        self.total = total
        if not force_calculate_base:
            self.is_valid_base()
        self.is_valid_logarithimand()

    def is_valid_base(self):
        if self.base is None:
            self.base = 10
        elif self.base <= 0 or self.base == 1:
            raise LogarithimError(
                "'base' must be positive and different of 1")
        return True

    def is_valid_logarithimand(self):
        if self.logarithimand is not None and self.logarithimand <= 0:
            raise LogarithimError(
                "'logarithimand' must be positive and different of 1")

    def evaluate(self):
        if not self.total:
            return self.calculate_total()
        elif self.base and self.total:
            self.calculate_logarithmand()
        else:
            self.calculate_base()

    def calculate_total(self):
        if self.total is not None:
            raise LogarithimError(
                "Total already given try to execute another function")
        factorin = Factorize()
        factorial_logarithimand = factorin.calculate_factorial(
            self.logarithimand)
        factorial_base = factorin.calculate_factorial(self.base)

        return True

    def anulate_factorial_each_other(self, factorial_left, factorial_right):
        for base, exponential in factorial_left.items():
            if base in factorial_right:
                exp_right = factorial_right[base]


    def calculate_logarithmand(self):
        raise NotImplementedError

    def calculate_base(self):
        raise NotImplementedError
