#!/usr/bin/python
from bot import createTweet
from bot import postStatus
from database import get_indices

for index in get_indices():
    tweet = createTweet(index[0], 'Risers', 'day')
    if (tweet != 'empty'):
        print(tweet)
        print(postStatus(tweet))
