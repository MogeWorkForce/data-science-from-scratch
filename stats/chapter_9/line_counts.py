# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import sys

count = 0

for line in sys.stdin:
    count += 1
    # print goes to sys.stdout
    print(count)
