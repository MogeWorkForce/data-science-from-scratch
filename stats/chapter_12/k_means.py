# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import math
import random
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

import re

from ..chapter_4.vectors import distance


def majority_vote(labels):
    """assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                       for count in vote_counts.values()
                       if count == winner_count])
    if num_winners == 1:
        return winner  # unique winner, so return it
    else:
        return majority_vote(labels[:-1])  # try again without the farthest


def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""
    # order the labeled points from nearest to farthest
    by_distance = sorted(
        labeled_points,
        key=lambda point, _: distance(point, new_point)
    )
    # find the labels for the k closest
    k_nearest_labels = [label for _, label in by_distance[:k]]
    # and let them vote
    return majority_vote(k_nearest_labels)


def plot_state_borders(plt, color='0.8'):
    pass


def random_point(dim):
    return [random.random() for _ in range(dim)]


def random_distances(dim, num_pairs):
    return [distance(random_point(dim), random_point(dim))
            for _ in range(num_pairs)]


cities = [(-86.75, 33.5666666666667, 'Python'),
          (-88.25, 30.6833333333333, 'Python'),
          (-112.016666666667, 33.4333333333333, 'Java'),
          (-110.933333333333, 32.1166666666667, 'Java'),
          (-92.2333333333333, 34.7333333333333, 'R'),
          (-121.95, 37.7, 'R'),
          (-118.15, 33.8166666666667, 'Python'),
          (-118.233333333333, 34.05, 'Java'),
          (-122.316666666667, 37.8166666666667, 'R'),
          (-117.6, 34.05, 'Python'),
          (-116.533333333333, 33.8166666666667, 'Python'),
          (-121.5, 38.5166666666667, 'R'),
          (-117.166666666667, 32.7333333333333, 'R'),
          (-122.383333333333, 37.6166666666667, 'R'),
          (-121.933333333333, 37.3666666666667, 'R'),
          (-122.016666666667, 36.9833333333333, 'Python'),
          (-104.716666666667, 38.8166666666667, 'Python'),
          (-104.866666666667, 39.75, 'Python'),
          (-72.65, 41.7333333333333, 'R'),
          (-75.6, 39.6666666666667, 'Python'),
          (-77.0333333333333, 38.85, 'Python'),
          (-80.2666666666667, 25.8, 'Java'),
          (-81.3833333333333, 28.55, 'Java'),
          (-82.5333333333333, 27.9666666666667, 'Java'),
          (-84.4333333333333, 33.65, 'Python'),
          (-116.216666666667, 43.5666666666667, 'Python'),
          (-87.75, 41.7833333333333, 'Java'),
          (-86.2833333333333, 39.7333333333333, 'Java'),
          (-93.65, 41.5333333333333, 'Java'),
          (-97.4166666666667, 37.65, 'Java'),
          (-85.7333333333333, 38.1833333333333, 'Python'),
          (-90.25, 29.9833333333333, 'Java'),
          (-70.3166666666667, 43.65, 'R'),
          (-76.6666666666667, 39.1833333333333, 'R'),
          (-71.0333333333333, 42.3666666666667, 'R'),
          (-72.5333333333333, 42.2, 'R'),
          (-83.0166666666667, 42.4166666666667, 'Python'),
          (-84.6, 42.7833333333333, 'Python'),
          (-93.2166666666667, 44.8833333333333, 'Python'),
          (-90.0833333333333, 32.3166666666667, 'Java'),
          (-94.5833333333333, 39.1166666666667, 'Java'),
          (-90.3833333333333, 38.75, 'Python'),
          (-108.533333333333, 45.8, 'Python'),
          (-95.9, 41.3, 'Python'),
          (-115.166666666667, 36.0833333333333, 'Java'),
          (-71.4333333333333, 42.9333333333333, 'R'),
          (-74.1666666666667, 40.7, 'R'),
          (-106.616666666667, 35.05, 'Python'),
          (-78.7333333333333, 42.9333333333333, 'R'),
          (-73.9666666666667, 40.7833333333333, 'R'),
          (-80.9333333333333, 35.2166666666667, 'Python'),
          (-78.7833333333333, 35.8666666666667, 'Python'),
          (-100.75, 46.7666666666667, 'Java'),
          (-84.5166666666667, 39.15, 'Java'), (-81.85, 41.4, 'Java'),
          (-82.8833333333333, 40, 'Java'), (-97.6, 35.4, 'Python'),
          (-122.666666666667, 45.5333333333333, 'Python'),
          (-75.25, 39.8833333333333, 'Python'),
          (-80.2166666666667, 40.5, 'Python'),
          (-71.4333333333333, 41.7333333333333, 'R'),
          (-81.1166666666667, 33.95, 'R'),
          (-96.7333333333333, 43.5666666666667, 'Python'),
          (-90, 35.05, 'R'), (-86.6833333333333, 36.1166666666667, 'R'),
          (-97.7, 30.3, 'Python'), (-96.85, 32.85, 'Java'),
          (-95.35, 29.9666666666667, 'Java'),
          (-98.4666666666667, 29.5333333333333, 'Java'),
          (-111.966666666667, 40.7666666666667, 'Python'),
          (-73.15, 44.4666666666667, 'R'),
          (-77.3333333333333, 37.5, 'Python'),
          (-122.3, 47.5333333333333, 'Python'),
          (-89.3333333333333, 43.1333333333333, 'R'),
          (-104.816666666667, 41.15, 'Java')]
cities = [([longitude, latitude], language) for
          longitude, latitude, language in cities]

WORDS_REGEX = re.compile(r"[a-z0-9']+")


def tokenize(message):
    message = message.lower()
    all_words = WORDS_REGEX.findall(message)
    return set(all_words)


def count_words(training_set):
    """training set consists of pairs (message, is_spam)"""
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in tokenize(message):
            counts[word][0 if is_spam else 1] += 1
    return counts


def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    """turn the word_counts into a list of triplets
    w, p(w | spam) and p(w | ~spam)"""
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
            for w, (spam, non_spam) in counts.items()]


def spam_probability(word_probs, message):
    message_words = tokenize(message)
    log_prob_if_spam = log_prob_if_not_spam = 0.0
    # iterate through each word in our vocabulary
    for word, prob_if_spam, prob_if_not_spam in word_probs:
        # if *word* appears in the message,
        # add the log probability of seeing it
        if word in message_words:
            log_prob_if_spam += math.log(prob_if_spam)
            log_prob_if_not_spam += math.log(prob_if_not_spam)

        # if *word* doesn't appear in the message
        # add the log probability of _not_ seeing it
        # which is log(1 - probability of seeing it)
        else:
            log_prob_if_spam += math.log(1.0 - prob_if_spam)
            log_prob_if_not_spam += math.log(1.0 - prob_if_not_spam)

    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)

    return prob_if_spam / (prob_if_spam + prob_if_not_spam)


class NaiveBayesClassifier:
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []

    def train(self, training_set):
        # count spam and non-spam messages
        num_spams = len([is_spam
                         for message, is_spam in training_set
                         if is_spam])
        num_non_spams = len(training_set) - num_spams
        # run training data through our "pipeline"
        word_counts = count_words(training_set)
        self.word_probs = word_probabilities(word_counts,
                                             num_spams,
                                             num_non_spams,
                                             self.k)

    def classify(self, message):
        return spam_probability(self.word_probs, message)


def p_spam_given_word(word_prob):
    """uses bayes's theorem to compute p(spam | message contains word)"""
    # word_prob is one of the triplets produced by word_probabilities
    word, prob_if_spam, prob_if_not_spam = word_prob
    return prob_if_spam / (prob_if_spam + prob_if_not_spam)

if __name__ == '__main__':
    # key is language, value is pair (longitudes, latitudes)
    plots = {"Java": ([], []), "Python": ([], []), "R": ([], [])}
    # we want each language to have a different marker and color
    markers = {"Java": "o", "Python": "s", "R": "^"}
    colors = {"Java": "r", "Python": "b", "R": "g"}
    for (longitude, latitude), language in cities:
        plots[language][0].append(longitude)
        plots[language][1].append(latitude)
    # create a scatter series for each language
    for language, (x, y) in plots.items():
        plt.scatter(x, y, color=colors[language], marker=markers[language],
                    label=language, zorder=10)
    plot_state_borders(plt)  # pretend we have a function that does this
    plt.legend(loc=0)
    plt.axis([-130, -60, 20, 55])  # let matplotlib choose the location
    # set the axes
    plt.title("Favorite Programming Languages")
    plt.show()
