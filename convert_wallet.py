import sys
import time

from config import ADDRESSES
import Binance_1
import keys
from balance_listener import deposit

bin = Binance_1.Binance(keys.key, keys.secret)
uid = sys.argv[1]
blockchain_1 = sys.argv[2]
blockchain_2 = sys.argv[3]
summ = float(sys.argv[4])
asset_from = sys.argv[5]
asset_to = sys.argv[6]

prev_balance = curr_balance = float(bin.get_spot_balance(asset_from))
deposit(blockchain_1, asset_from, summ)

while curr_balance * 0.99 < prev_balance:
    time.sleep(60)
    curr_balance = float(bin.get_spot_balance(asset_from))

summ = min(summ, curr_balance)
balance_from = bin.get_spot_balance('USDT')
if asset_from != "USDT":

    bin.open_spot_position(asset_from + 'USDT', 'SELL', summ, 'MARKET', uid)
    time.sleep(3)
balance_to = bin.get_spot_balance('USDT')
qty = (float(balance_to) - float(balance_from)) / float(bin.client.latest_information_for_symbol(
    symbol=asset_to + 'USDT')["result"][0]["last_price"]) * 0.99

token_balance_from = bin.get_spot_balance(asset_to)
bin.open_spot_position(asset_to + 'USDT', 'BUY', qty, 'MARKET', uid)
time.sleep(3)
token_balance_to = bin.get_spot_balance(asset_to)
token_summ = min(float(token_balance_to) -
                 float(token_balance_from), bin.get_spot_balance(asset_to))

bin.withdraw(asset_to, token_summ, ADDRESSES[blockchain_2], blockchain_2)
