# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import os

from collections import Counter

from twython import Twython
from .streamer import CustomStreamerTwitter

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]


if __name__ == "__main__":
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)

    # search for tweets containing the phrase "data science"
    for status in twitter.search(q='colunaflamengo')["statuses"]:
        user = status["user"]["screen_name"]
        text = status["text"]
        print("%s:%s\n" % (user, text))

    stream = CustomStreamerTwitter(CONSUMER_KEY, CONSUMER_SECRET,
                                   ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                                   limit=150)
    # starts consuming public statuses that contain the keyword 'data'
    try:
        stream.statuses.filter(track='data')
    except:
        pass
    # if instead we wanted to start consuming a sample of *all* public statuses
    # stream.statuses.sample()

    top_hashtags = Counter(hashtag['text'].lower()
                           for tweet in stream.tweets
                           for hashtag in tweet["entities"]["hashtags"])
    print(top_hashtags.most_common(5))
