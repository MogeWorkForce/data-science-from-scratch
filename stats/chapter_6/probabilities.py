# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import random

gender = ["boy", "girl"]
dice_faces = list(range(1, 7))

# G = Gold, W = wood, S = spades, H = heart
card_suit = "GWSH"
deck = []
for suit in card_suit:
    deck.extend([str(i)+suit for i in range(1, 14)])


def random_kid():
    return random.choice(gender)


def valid_sample(positive_events, type_events):
    real_events = [
        x for x in type_events
        if x in positive_events
    ]

    return real_events


def probability(positive_events, type_events, exclude_n_event=0,
                keep_desired_events=False):
    events = valid_sample(positive_events, type_events)
    desired_events = len(events)
    if not keep_desired_events and exclude_n_event > 0:
        desired_events = len(events) - exclude_n_event
    total_events_in_analysis = len(type_events) - exclude_n_event
    return desired_events / total_events_in_analysis


def oposite_probability(positive_events, type_events):
    negative_events = [
        x for x in type_events
        if x not in positive_events
    ]
    return probability(negative_events, type_events)


def probability_of_multiple_events(desired_outcomes, type_events,
                                   remove_from_events=False,
                                   keep_desired_events=False):
    """
        Simple formula to calculate probability of multiple events.
        When `remove_from_events = True`, it's indicate of that outcome
        must be removed from the possible events.
        Ex:
            We have deck of cards (52 cards), and with consecutive draw,
            we will continue to get a next card without put again on deck
            the previous drawed card, so the number of possible events
            will decrease.
    """
    result = 1
    exclude_n_events = 0
    for outcome in desired_outcomes:
        result *= probability(
            outcome, type_events, exclude_n_events, keep_desired_events)
        if remove_from_events:
            exclude_n_events += 1

    return result


def conditional_probability(outcomes, events_list):
    """
        Outcomes must be a list with 2 dimensions
    """
    result = 1
    for i, outcome_event_zipped in enumerate(zip(outcomes, events_list)):
        outcome, events = outcome_event_zipped
        current_probability = probability(outcome, events)
        if i == 0:
            result *= current_probability
        else:
            result /= current_probability
    return result


if __name__ == "__main__":
    both_girls = 0
    older_girl = 0
    either_girl = 0

    random.seed(0)
    print("Probability to get a girl in one event:",
          probability(gender[:1], gender))
    print("Probability of does not get a girl in one event:",
          oposite_probability(gender[:1], gender))
    for _ in range(10000):
        younger = random_kid()
        older = random_kid()
        if older == "girl":
            older_girl += 1
        if older == "girl" and younger == "girl":
            both_girls += 1
        if older == "girl" or younger == "girl":
            either_girl += 1

    print(both_girls, older_girl, either_girl)
    print("P(both | older):", both_girls / older_girl)
    print("P(both | either):", both_girls / either_girl)

    print("-" * 10)
    desired_outputs = [1, 4]
    print("Probabilities when roll dice in one event lower or equals than sample:", desired_outputs,
          probability(desired_outputs, dice_faces))
    print("Probabilities when roll dice in one event is not lower or equals than sample:", desired_outputs,
          oposite_probability(desired_outputs, dice_faces))

    print("-" * 10)
    # In first event
    desired_outcomes = [
        [1], [1]
    ]
    p_dices = probability_of_multiple_events(desired_outcomes, dice_faces)
    print(
        "Probabilities when first events is equal %r and second %r is: %.2f"
        % (
            desired_outcomes[0],
            desired_outcomes[1],
            p_dices * 100
        )
    )

    print("-" * 10)

    desired_outcomes = [
        [str(i)+card_suit[0] for i in range(1, 14)],
        [str(i)+card_suit[0] for i in range(1, 14)]
    ]
    p_cards = probability_of_multiple_events(
        desired_outcomes, deck, remove_from_events=True)
    print(
        "Probabilities when first events is equal %r and second %r is: %.2f"
        % (
            desired_outcomes[0],
            desired_outcomes[1],
            p_cards * 100
        )
    )

    print("-" * 10)
    print("Multiple alternatives with decrease total events, but changing"
          " desired events.")
    blues = ["B" for _ in range(5)]
    whites = ["W" for _ in range(4)]
    reds = ["R" for _ in range(11)]
    all_balls = []
    all_balls.extend(blues)
    all_balls.extend(reds)
    all_balls.extend(whites)
    desired_outcomes = [
        blues,
        whites,
        reds
    ]

    p_balls = probability_of_multiple_events(
        desired_outcomes, all_balls, remove_from_events=True,
        keep_desired_events=True)
    print(
        "Probabilities when %r desired outcomes: %.2f"
        % (
            desired_outcomes,
            p_balls * 100
        )
    )

    events_list = [
        deck,
        deck
    ]

    outcomes = [
        ["1S"],
        [x for x in deck if "S" in x]
    ]

    p_spades = conditional_probability(outcomes, events_list)

    print(
        "Probabilities Conditional when %r desired outcomes: %.2f"
        % (
            outcomes,
            p_spades * 100
        )
    )
