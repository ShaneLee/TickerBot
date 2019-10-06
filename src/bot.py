#!/usr/bin/python
from config import getApi
from database import get_top_biggest_risers_previous_day_by_index
from database import get_top_biggest_fallers_previous_day_by_index
from database import get_top_biggest_risers_previous_week_by_index
from database import get_top_biggest_fallers_previous_week_by_index
from database import get_top_biggest_200_day_mean_by_index
from database import get_top_biggest_risers_international_previous_day_by_index
from database import get_top_biggest_fallers_international_previous_day_by_index
from database import get_top_biggest_risers_international_previous_week_by_index
from database import get_top_biggest_fallers_international_previous_week_by_index
from database import get_indices
from database import get_db_keys
from babel.numbers import format_decimal
from datetime import date
from decimal import Decimal
import os

NUM = 5

api = getApi()
db_keys = get_db_keys()

def round_decimal(x):
    decimal_value = Decimal(x)
    return decimal_value.quantize(Decimal(10) ** -2)

def postStatus(update):
    status = api.PostUpdate(update)
    print(status)

def postWithImage(update, media):
    print(api.PostUpdate(update, media=media))
    os.remove(media)

def get_change(open, close):
    return str(round_decimal(((close / open) * 100) - 100.00))

def getData(index, direction, period):
    if (period == 'day'):
        return get_top_biggest_risers_previous_day_by_index(index, NUM) if direction == 'Risers' else get_top_biggest_fallers_previous_day_by_index(index, NUM)
    return get_top_biggest_risers_previous_week_by_index(index, NUM) if direction == 'Risers' else get_top_biggest_fallers_previous_week_by_index(index, NUM)

def getUsaData(index, direction, period):
    if (period == 'day'):
        return get_top_biggest_risers_international_previous_day_by_index(index, NUM, '') if direction == 'Risers' else get_top_biggest_fallers_international_previous_day_by_index(index, NUM, '')
    return get_top_biggest_risers_international_previous_week_by_index(index, NUM, '') if direction == 'Risers' else get_top_biggest_fallers_international_previous_week_by_index(index, NUM, '')


def createTweet(index, direction, period):
    data = getData(index, direction, period)
    if (len(data) == 0):
        return 'empty'
    tweet = 'Biggest #' + index + ' ' + direction + ' ' + date.today().strftime("%d/%m/%Y") + '\n'
    hash_tags = ''
    for i, d in enumerate(data[0:5]):
        ticker_hashtag = '#' + d[db_keys["ticker"]]
        name = d[db_keys["name"]]
        close_price = d[db_keys["close"]]
        change = get_change(d[db_keys["open"]], d[db_keys["close"]])+'%'
        mean_200_days = d[db_keys["long_mean"]]
        row = str(i+1) + '. ' + name + ' Close: ' + str(close_price) + ' ' + change
        tweet = tweet + row + '\n'
        hash_tags = hash_tags + ticker_hashtag + ' '
    if (len(tweet) + len(hash_tags) <= 239):
        return tweet + '\n' + hash_tags
    return tweet

def createUsaTweet(index, direction, period):
    data = getUsaData(index["index_code"], direction, period)
    if (len(data) == 0):
        return 'empty'
    tweet = 'Biggest #' + index['index_name'] + ' ' + direction + ' ' + date.today().strftime("%d/%m/%Y") + '\n'
    hash_tags = ''
    for i, d in enumerate(data[0:5]):
        ticker_hashtag = '$' + d[db_keys["ticker"]]
        name = d[db_keys["name"]]
        close_price = d[db_keys["close"]]
        change = get_change(d[db_keys["open"]], d[db_keys["close"]])+'%'
        mean_200_days = d[db_keys["long_mean"]]
        row = str(i+1) + '. ' + name + ' Close: ' + str(close_price) + ' ' + change
        tweet = tweet + row + '\n'
        hash_tags = hash_tags + ticker_hashtag + ' '
    if (len(tweet) + len(hash_tags) <= 239):
        return tweet + '\n' + hash_tags
    return tweet

def createMovingMeanTweet(index):
    data = get_top_biggest_200_day_mean_by_index(index, NUM)
    if (len(data) == 0):
        return 'empty'
    tweet = 'Largest -% 200 Day Mean #' + index + '\n'
    hash_tags = ''
    for i, d in enumerate(data[0:5]):
        ticker_hashtag = '#' + d[1]
        name = d[18]
        long_mean_percent_diff = str(round_decimal(d[6])) + '%'
        long_mean = str(d[5])
        row = str(i+1) + '. ' + name + ' 200D Mean: ' + str(long_mean) + ' ' + long_mean_percent_diff
        tweet = tweet + row + '\n'
        hash_tags = hash_tags + ticker_hashtag + ' '
    if (len(tweet) + len(hash_tags) <= 239):
        return tweet + '\n' + hash_tags
    return tweet

def createTweetWithImage(data):
    hash_tag = '$' + data['ticker'] if data['country'] == 'USA' else '#' + data['ticker']
    tweet = '365 Day Monte Carlo Simulation for ' + data['name'] + '\n Last Close: ' + data['last_close'] + '\n Mean 365 Price: ' + data['mean_365_day_price'] + '\n 365 % Diff: ' + data['pct'] + '\n' + hash_tag
    postWithImage(tweet, 'tempplot.png')
