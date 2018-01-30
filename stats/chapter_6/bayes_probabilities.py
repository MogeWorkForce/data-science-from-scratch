# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
import random
from . import probabilities


decease_events = [0 for _ in range(10000)]
decease_events[-1] = 1

test_events = [0 for _ in range(100)]
test_events[-1] = 1


def bayes_law(p_a, p_b_a, p_b_not_a, not_a):
    return (p_b_a * p_a)/((p_b_a * p_a) + (p_b_not_a * not_a))


if __name__ == "__main__":
    decease_counts = 0
    test_positive_counts = 0
    desease_positive_counts = 0
    no_decease_positive_counts = 0
    random.seed(0)
    for _ in range(1000000):
        d = random.choice(decease_events)
        t = random.choice(test_events)

        if d == 1 and t == 0:
            desease_positive_counts += 1

        if d == 0 and t == 1:
            no_decease_positive_counts += 1

    print("Total deceases with positive test: ", desease_positive_counts)
    print("Total deceases with positive test (%): ", (desease_positive_counts / 1000000) * 100)
    print("Total no deceases with positive test: ", no_decease_positive_counts)

    microwaves_broken = [1, 0, 0, 0]
    # pa = 0.25
    really_broken = probabilities.probability([1], microwaves_broken)
    not_broken = probabilities.oposite_probability([1], microwaves_broken)

    # pba = 0.9
    possibles_diagnostics = []
    undefined_diagnostic = [None for _ in range(5)]
    correct_diagnostic = [1 for _ in range(90)]
    wrong_diagnostic = [0 for _ in range(5)]
    possibles_diagnostics.extend(undefined_diagnostic)
    possibles_diagnostics.extend(correct_diagnostic)
    possibles_diagnostics.extend(wrong_diagnostic)

    # pba = 0.9
    # Probability: given microwaves really broken,
    # the professional give correct diagnostic (microwave broken)
    pba = probabilities.probability([1], possibles_diagnostics)

    # pbnota = 0.05
    # Probability: given microwaves did not broken,
    # the professional give incorrect diagnostic
    # (tell you that microwave was broken)
    pbnota = 0.05

    # Expected 85.7 %
    print(bayes_law(really_broken, pba, pbnota, not_broken))
