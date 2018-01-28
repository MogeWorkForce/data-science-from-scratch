# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
import random


decease_events = [0 for _ in range(10000)]
decease_events[-1] = 1

test_events = [0 for _ in range(100)]
test_events[-1] = 1


if __name__ == "__main__":
    decease_counts = 0
    test_positive_counts = 0
    decease_positive_counts = 0
    no_decease_positive_counts = 0
    random.seed(0)
    for _ in range(1000000):
        d = random.choice(decease_events)
        t = random.choice(test_events)

        if d == 1 and t == 0:
            decease_positive_counts += 1

        if d == 0 and t == 1:
            no_decease_positive_counts += 1

    print("Total deceases with positive test: ", decease_positive_counts)
    print("Total deceases with positive test (%): ", (decease_positive_counts / 1000000) * 100)
    print("Total no deceases with positive test: ", no_decease_positive_counts)
