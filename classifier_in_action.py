# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import glob
import random
import re
import json

from collections import Counter

from stats.chapter_11.linear_regression import split_data
from stats.chapter_12.k_means import NaiveBayesClassifier
from stats.chapter_12.k_means import p_spam_given_word

"""
WARNING: you need to download these files in order to execute this script
http://spamassassin.apache.org/old/publiccorpus/
(20021010_*)
Unpacking them inside folder called "spam", like this:
├── spam
│   ├── easy_ham
│   ├── hard_ham
│   └── spam

"""
path = "/home/hermogenes/Devs/personal_dev/spam/*/*"
print(path)

data = []
# glob.glob returns every filename that matches the wildcarded path
for fn in glob.glob(path):
    is_spam = "ham" not in fn
    with open(fn, 'r') as file:
        for line in file:
            if line.startswith("Subject:"):
                # remove the leading "Subject: " and keep what's left
                subject = re.sub(r"^Subject: ", "", line).strip()
                data.append((subject, is_spam))

random.seed(0, version=1)  # just so you get the same answers as me
train_data, test_data = split_data(data, 0.75)
classifier = NaiveBayesClassifier()
classifier.train(train_data)

# triplets (subject, actual is_spam, predicted spam probability)
classified = [(subject, is_spam, classifier.classify(subject))
              for subject, is_spam in test_data]
# assume that spam_probability > 0.5 corresponds to spam prediction
# and count the combinations of (actual is_spam, predicted is_spam)
counts = Counter((is_spam, spam_probability > 0.5)
                 for _, is_spam, spam_probability in classified)

print(counts)

# sort by spam_probability from smallest to largest
classified.sort(key=lambda row: row[2])

# the highest predicted spam probabilities among the non-spams
spammiest_hams = list(filter(lambda row: not row[1], classified))[-5:]
# the lowest predicted spam probabilities among the actual spams
hammiest_spams = list(filter(lambda row: row[1], classified))[:5]

# print(json.dumps(spammiest_hams, indent=2))
# print(json.dumps(hammiest_spams, indent=2))

words = sorted(classifier.word_probs, key=p_spam_given_word)
spammiest_words = words[-5:]
hammiest_words = words[:5]

print(json.dumps(spammiest_words, indent=2))
print(json.dumps(hammiest_words, indent=2))
