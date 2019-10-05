#!/usr/bin/python
from bot import createMovingMeanTweet
from bot import postStatus
from database import get_indices

for index in get_indices():
    tweet = createMovingMeanTweet(index[0])
    if (tweet != 'empty'):
        print(tweet)
        print(postStatus(tweet))
