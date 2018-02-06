# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

from twython import TwythonStreamer


# appending data to a global variable is pretty poor form
# but it makes the example much simpler


class CustomStreamerTwitter(TwythonStreamer):
    """our own subclass of TwythonStreamer that specifies
    how to interact with the stream"""
    tweets = []

    def __init__(self, *args, **kwargs):
        self.limit = kwargs.pop("limit", 1000)
        super(CustomStreamerTwitter, self).__init__(*args, **kwargs)

    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python dict representing a tweet"""

        # only want to collect English-language tweets
        if data['lang'] == 'en':
            self.tweets.append(data)
        print("received tweet #", len(self.tweets))
        # stop when we've collected enough
        if len(self.tweets) >= self.limit:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()
