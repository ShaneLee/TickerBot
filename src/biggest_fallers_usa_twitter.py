#!/usr/bin/python
from bot import createUsaTweet
from bot import postStatus
from database import get_usa_indices

for index in get_usa_indices():
    tweet = createUsaTweet(index, 'Fallers', 'day')
    if (tweet != 'empty'):
        print(tweet)
        print(postStatus(tweet))
