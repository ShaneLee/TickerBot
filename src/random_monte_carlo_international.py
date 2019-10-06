#!/usr/bin/python
from bot import createTweetWithImage
from database import get_international_stocks
from monte_carlo import get_simulation
import random
import os

stocks = get_international_stocks()
stock = random.choice(stocks)

print(stock[1])
country = stock[6]
ticker = stock[0] + '.' + stock[7] if len(stock[7]) > 0 else stock[0]
createTweetWithImage(get_simulation(ticker, stock[1], country))
