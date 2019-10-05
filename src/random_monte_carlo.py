#!/usr/bin/python
from bot import createTweetWithImage
from database import get_stocks
from monte_carlo import get_simulation
import random
import os

stocks = get_stocks()
stock = random.choice(stocks)

print(stock[1])
createTweetWithImage(get_simulation(stock[0], stock[1]))
