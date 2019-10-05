#!/usr/bin/python
from database import get_biggest_trades
from bot import postStatus
from babel.numbers import format_decimal
from datetime import date

def createTweet():
    data = get_biggest_trades(3)
    tweet = 'Biggest UK Trades ' + date.today().strftime("%d/%m/%Y") + '\n'
    hash_tags = ''
    for i, d in enumerate(data[0:5]):
        ticker_hashtag = '#' + d[1]
        name = d[10]
        trade_price = d[3]
        trade_quantity = d[4]
        trade_value = format_decimal(d[9], locale='en_GB')
        buy_sell = d[8]
        row = str(i+1) + '. ' + name + ' ' + buy_sell + ' ' + unichr(163) + trade_value
        tweet = tweet + row + '\n'
        hash_tags = hash_tags + ticker_hashtag + ' '
    if (len(tweet) + len(hash_tags) <= 239):
        return tweet + '\n' + hash_tags
    return tweet


tweet = createTweet()
print(tweet)
print(postStatus(tweet))
