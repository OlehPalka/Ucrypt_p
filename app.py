import copy
import balance_listener
import requests
from flask import *
from flask_cors import cross_origin
from balance_listener import *
import json
import uc_db_clients_sql
import mongo_db_futures_trading
import mongo_db_spot_trading
import Binance_1
import keys
import time
import os
import psycopg2
from binance import Client
import time
from config import *
bin = Binance_1.Binance(keys.key, keys.secret)

app = Flask(__name__)


@app.route("/createUser", methods=["POST"])
@cross_origin()
def create():
    try:
        data = request.json()
    except:
        data = request.json

    uc_db_clients_sql.add_client(data['email'], data["password"], data['pin'])
    user_data = uc_db_clients_sql.find_user_by_email(data['email'])
    print(user_data)
    mongo_db_spot_trading.add_new_client(user_data[0], user_data[1], "_")
    mongo_db_futures_trading.add_new_client(user_data[0], user_data[1])

    result = {"relevantEmailAndPassword": True, "userId": user_data[0]}
    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/getUser", methods=["POST"])
@cross_origin()
def get_user():
    try:
        data = request.json()
    except:
        data = request.json
    result = {}
    try:
        user_data = uc_db_clients_sql.find_user_by_email(data['email'])
        if user_data[1] == data['email'] and user_data[2] == data['password']:
            result["relevantEmailAndPassword"] = True
            result['user_id'] = user_data[0]
        else:
            result["relevantEmailAndPassword"] = False

        if user_data[3] == data['pin']:
            result["relevantPin"] = True
        else:
            result["relevantPin"] = False

    except:
        result = {"relevantEmailAndPassword": False,
                  "relevantPin": False}

    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/userProfile", methods=["POST"])
@cross_origin()
def user_profile():
    try:
        data = request.json()
    except:
        data = request.json
    id = int(data['userId'])

    try:
        name = data['name']
        uc_db_clients_sql.change_name(id, name)
    except Exception:
        name = uc_db_clients_sql.find_user_by_id(id)[-2]
        pass

    try:
        avatar = data['avatar']
        uc_db_clients_sql.change_image(id, avatar)
    except Exception:
        avatar = uc_db_clients_sql.find_user_by_id(id)[-1]
        pass

    result = {"avatar": avatar,
              "name": name}

    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/getAllBalances", methods=["POST"])
@cross_origin()
def get_all_balances():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])

    binance_balances = Client(keys.key, keys.secret).get_account()['balances']

    prices = Client(
        keys.key, keys.secret).get_all_tickers()

    all_coins_bal = {}
    for i in binance_balances:
        if float(i["free"]) > 0:
            all_coins_bal[i['asset']] = i["free"]

    # for coin_info in binance_balances:
    #     coin_name = coin_info['asset']
    #     if coin_name == "USDT":
    #         amount = float(coin_info['free'])
    #         spot_usdt_bal = float(coin_info['free'])
    #         all_coins_bal[coin_name] = amount
    #     else:
    #         amount = float(coin_info['free'])
    #         if amount > 0:
    #             all_coins_bal[coin_name] = f"{amount:.9f}"

    # mongo_db_spot_trading.change_all_different_coins_balance(id, all_coins_bal)

    # for coin_info in binance_balances:
    #     coin_name = coin_info['asset']
    #     amount = float(coin_info['free'])
    #     try:
    #         if amount > 0:
    #             pair = coin_name + "USDT"
    #             key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    #             data = requests.get(key)
    #             data = data.json()
    #             cur_price = float(data['price'])
    #             spot_usdt_bal += cur_price * amount
    #     except Exception:
    #         continue
    try:
        spot_usdt_bal = float(all_coins_bal["USDT"])
    except Exception:
        spot_usdt_bal = 0

    for coin_info in prices:
        if "USDT" in coin_info['symbol']:
            coin = coin_info['symbol'].replace("USDT", "")
            if coin in all_coins_bal:
                price = float(coin_info['price'])
                amount = float(all_coins_bal[coin])
                spot_usdt_bal += price * amount

    all_coins = []
    for i in all_coins_bal:
        all_coins.append({"symbol": i,
                          "balance": all_coins_bal[i]})

    result = {"UserId": id, "infoOfAllCoins": all_coins,
              'balance': spot_usdt_bal}

    fut_balance = mongo_db_futures_trading.get_balance(id)
    crypto_api_bal = balance_listener.get_balances()

    result = {"spotUsdtBalance": spot_usdt_bal, "AllCoinsSpotBalance": all_coins_bal, "futuresBalance": fut_balance,
              "crypto_api_bal": crypto_api_bal}

    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/wallet", methods=["POST"])
@cross_origin()
def wallet():
    try:
        data = request.json()
    except:
        data = request.json
    id = int(data['UserId'])

    crypt_api = balance_listener.get_balances()
    usdt_balance = 0
    for i in crypt_api:
        if "USDT" in crypt_api[i]:
            usdt = float(crypt_api[i]['USDT'])
            usdt_balance += usdt

    prices = Client(
        keys.key, keys.secret).get_all_tickers()

    wallet_bals = get_balances()
    wallet_coins_bals = {}
    for blockch in wallet_bals:
        for coin_name in wallet_bals[blockch]:
            if coin_name != "USDT":
                if coin_name != "TRX" and blockch != 'tron':
                    if coin_name != "BNB" and blockch != 'binance-smart-chain':
                        if coin_name != "ETH" and blockch != 'ethereum':
                            amount = wallet_bals[blockch][coin_name]
                            wallet_coins_bals[coin_name] = amount

    for coin_info in prices:
        if "USDT" in coin_info['symbol']:
            coin = coin_info['symbol'].replace("USDT", "")
            if coin in wallet_coins_bals:
                price = float(coin_info['price'])
                amount = float(wallet_coins_bals[coin])
                usdt_balance += price * amount

    result = {"balance": usdt_balance, "infoOfAllCoins": crypt_api}

    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/spot", methods=["POST"])
@cross_origin()
def spot():

    start_time = time.time()

    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])

    # all_coins_bal = mongo_db_spot_trading.get_different_coins_balances(id)

    binance_balances = Client(keys.key, keys.secret).get_account()['balances']

    prices = Client(
        keys.key, keys.secret).get_all_tickers()

    all_coins_bal = {}
    for i in binance_balances:
        if float(i["free"]) > 0:
            all_coins_bal[i['asset']] = i["free"]

    # for coin_info in binance_balances:
    #     coin_name = coin_info['asset']
    #     if coin_name == "USDT":
    #         amount = float(coin_info['free'])
    #         spot_usdt_bal = float(coin_info['free'])
    #         all_coins_bal[coin_name] = amount
    #     else:
    #         amount = float(coin_info['free'])
    #         if amount > 0:
    #             all_coins_bal[coin_name] = f"{amount:.9f}"

    # mongo_db_spot_trading.change_all_different_coins_balance(id, all_coins_bal)

    # for coin_info in binance_balances:
    #     coin_name = coin_info['asset']
    #     amount = float(coin_info['free'])
    #     try:
    #         if amount > 0:
    #             pair = coin_name + "USDT"
    #             key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    #             data = requests.get(key)
    #             data = data.json()
    #             cur_price = float(data['price'])
    #             spot_usdt_bal += cur_price * amount
    #     except Exception:
    #         continue
    try:
        spot_usdt_bal = float(all_coins_bal["USDT"])
    except Exception:
        spot_usdt_bal = 0

    for coin_info in prices:
        if "USDT" in coin_info['symbol']:
            coin = coin_info['symbol'].replace("USDT", "")
            if coin in all_coins_bal:
                price = float(coin_info['price'])
                amount = float(all_coins_bal[coin])
                spot_usdt_bal += price * amount

    all_coins = []
    for i in all_coins_bal:
        all_coins.append({"symbol": i,
                          "balance": all_coins_bal[i]})

    result = {"UserId": id, "infoOfAllCoins": all_coins,
              'balance': spot_usdt_bal}
    print("--- %s seconds ---" % (time.time() - start_time))

    return json.dumps(result), 200, {"ContentType": "application/json"}


@app.route("/openSpotOrder", methods=["POST"])
@cross_origin()
def openSpotOrder():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    side = data["longOrShort"]
    money = data['replenishment']

    key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    data = requests.get(key)
    data = data.json()
    cur_price = float(data['price'])
    qnt = money/cur_price

    bin.open_spot_position(pair, side, qnt, 'MARKET', id)

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/futures", methods=["POST"])
@cross_origin()
def futures():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])

    db_positions = mongo_db_futures_trading.get_positions(id)
    positions = copy.deepcopy(db_positions)
    db_open_orders = mongo_db_futures_trading.get_limit_positions(id)
    balance = mongo_db_futures_trading.get_balance(id)
    open_orders = copy.deepcopy(db_open_orders)

    for pair in db_positions:
        for side in db_positions[pair]:
            if db_positions[pair][side] == []:
                del positions[pair][side]

    for pair in db_open_orders:
        for side in db_open_orders[pair]:
            if open_orders[pair][side]['LIMIT'] == {}:
                del open_orders[pair][side]['LIMIT']
            if open_orders[pair][side]['STOP_MARKET'] == {}:
                del open_orders[pair][side]['STOP_MARKET']
            if open_orders[pair][side]['TAKE_PROFIT_MARKET'] == {}:
                del open_orders[pair][side]['TAKE_PROFIT_MARKET']
            if open_orders[pair][side]['LIQUIDATION'] == {}:
                del open_orders[pair][side]['LIQUIDATION']

            if open_orders[pair][side] == {}:
                del open_orders[pair][side]
        if open_orders[pair] == {}:
            del open_orders[pair]

    return json.dumps({"balance": balance, "positions": positions, "openOrders": open_orders}), 200, {"ContentType": "application/json"}


@app.route("/editFuturesPosition", methods=["POST"])
@cross_origin()
def editFuturesPosition():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    openFuturesTakeProffit = data['openFuturesTakeProffit']
    openFuturesStopLoss = data['openFuturesStopLoss']
    side = data['side']  # BUY SELL
    sum_stop = data['sum_stop']
    sum_take = data['sum_take']
    qnt_stop = mongo_db_futures_trading.get_positions(id)[pair][side][1]
    qnt_take = mongo_db_futures_trading.get_positions(id)[pair][side][1]
    leverage = data['leverage']
    isol_cros = data['cros']  # ISOLATED CROS
    stop = "_"
    take = "_"
    if openFuturesStopLoss != 'undefined':
        stop = bin.open_futures_stoploss_position(pair, side, qnt_stop, float(
            openFuturesStopLoss), id, leverage, isol_cros)["clientOrderId"]
    if openFuturesTakeProffit != 'undefined':
        take = bin.open_futures_takeprofit_position(pair, side, qnt_take, float(
            openFuturesTakeProffit), id, leverage, isol_cros)["clientOrderId"]

    return json.dumps({"take_id": take, "stop_id": stop}), 200, {"ContentType": "application/json"}


@app.route("/closeFuturesPosition", methods=["POST"])
@cross_origin()
def closeFuturesPosition():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    side = data['side']  # BUY SELL
    qnt = (data['sum'] / data['price']) * data['leverage']
    leverage = data['leverage']

    bin.close_part_of_open_position_market(pair, side, qnt, id, leverage)

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/createFuturesPosition", methods=["POST"])
@cross_origin()
def createFuturesPosition():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    side = data['longOrShort']  # BUY SELL
    qnt = (data['replenishment'] / data['price']) * data['leverage']
    leverage = data['leverage']
    isol_cros = data['crossOrIsolate']
    limit_market = data["limitOrMarket"]
    price = data['price']
    pose = bin.open_futures_position(
        pair, side, qnt, limit_market, id, leverage, isol_cros, price)

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/cancelOrder", methods=["POST"])
@cross_origin()
def cancelOrder():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    order_id = data['orderId']
    bin.cancel_open_futures_order(pair, order_id)

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/send", methods=["POST"])
@cross_origin()
def send():
    try:
        data = request.json()
    except:
        data = request.json

    bin_2 = Binance_1.Binance('...',
                              '...')

    id = int(data['UserId'])
    send_point = data['send_point']
    blockchain = data["blockchain"]
    sum = data["sum"]
    pair = data['pair']
    address = data['address']

    if send_point == "spot":
        bin.withdraw(pair, sum, address, blockchain)
    elif send_point == "wallet":
        balance_listener.withdraw(blockchain, address, pair, sum)
    elif send_point == "invest":
        bin_2.withdraw(pair, sum, address, blockchain)

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/invest", methods=["POST"])
@cross_origin()
def invest():
    try:
        data = request.json()
    except:
        data = request.json

    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])

    # all_coins_bal = mongo_db_spot_trading.get_different_coins_balances(id)

    binance_balances = Client('...',
                              '...').get_account()['balances']

    prices = Client('...',
                    '...').get_all_tickers()

    all_coins_bal = {}
    for i in binance_balances:
        if float(i["free"]) > 0:
            all_coins_bal[i['asset']] = i["free"]

    try:
        spot_usdt_bal = float(all_coins_bal["USDT"])
    except Exception:
        spot_usdt_bal = 0

    for coin_info in prices:
        if "USDT" in coin_info['symbol']:
            coin = coin_info['symbol'].replace("USDT", "")
            if coin in all_coins_bal:
                price = float(coin_info['price'])
                amount = float(all_coins_bal[coin])
                spot_usdt_bal += price * amount

    all_coins = []
    for i in all_coins_bal:
        all_coins.append({"symbol": i,
                          "balance": all_coins_bal[i]})

    return json.dumps({"balance": spot_usdt_bal}), 200, {"ContentType": "application/json"}


@app.route("/convert", methods=["POST"])
@cross_origin()
def convert():
    "поменять ЮСДТ на любую монетку"
    try:
        data = request.json()
    except:
        data = request.json

    bin_2 = Binance_1.Binance(
        '...', '...')

    id = int(data['UserId'])
    send_point = data['send_point']
    destination_point = data['destination_point']
    blockchain_1 = data["blockchain_1"] if "blockchain_1" in data else data["blockchain"]
    blockchain_2 = data["blockchain_2"] if "blockchain_2" in data else data["blockchain"]
    sum = data["sum"]
    asset = data['asset']

    try:
        address = data["address"]
    except Exception:
        pass

    if send_point == 'wallet' and destination_point == "spot":
        balance_listener.deposit(blockchain_1, asset, sum)

    elif send_point == 'wallet' and destination_point == "futures":
        balance_listener.deposit(blockchain_1, asset, sum)
        prev_balance = curr_balance = float(bin.get_spot_balance(asset))
        while curr_balance <= prev_balance:
            time.sleep(60)
            curr_balance = float(bin.get_spot_balance(asset))
        bin.transfer_spot_to_futures(sum, "USDT")
        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        futures_bal += sum
        mongo_db_futures_trading.change_balance(id, futures_bal)

    elif send_point == 'spot' and destination_point == "futures":
        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        bin.transfer_spot_to_futures(sum, "USDT")
        futures_bal += sum
        mongo_db_futures_trading.change_balance(id, futures_bal)
    elif send_point == 'futures' and destination_point == "spot":
        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        bin.transfer_futures_to_spot(sum, "USDT")
        futures_bal -= sum
        mongo_db_futures_trading.change_balance(id, futures_bal)
    elif send_point == 'futures' and destination_point == "wallet":
        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        futures_bal -= sum
        mongo_db_futures_trading.change_balance(id, futures_bal)
        bin.transfer_futures_to_spot(sum, "USDT")
        address = ADDRESSES[blockchain_2]
        bin.withdraw("USDT", sum, address, blockchain_2)
    elif send_point == 'spot' and destination_point == "wallet":
        address = ADDRESSES[blockchain_2]
        bin.withdraw(asset, sum, address, blockchain_2)
    elif send_point == 'spot' and destination_point == "invest":
        address = BINANCE_INVEST_ADDRESSES[blockchain_2]
        bin.withdraw(asset, sum, address, blockchain_2)
    elif send_point == 'wallet' and destination_point == "invest":
        address = BINANCE_INVEST_ADDRESSES[blockchain_2]
        balance_listener.withdraw(blockchain_1, address, asset, sum)
    elif send_point == 'futures' and destination_point == "invest":
        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        futures_bal -= sum
        mongo_db_futures_trading.change_balance(id, futures_bal)
        bin.transfer_futures_to_spot(sum, "USDT")
        address = BINANCE_INVEST_ADDRESSES[blockchain_2]
        bin.withdraw("USDT", sum, address, blockchain_1)
    elif send_point == 'invest' and destination_point == "spot":
        address = BINANCE_ADDRESSES[blockchain_2]
        bin_2.withdraw(asset, sum, address, blockchain_1)
    elif send_point == 'invest' and destination_point == "wallet":
        address = ADDRESSES[blockchain_2]
        bin_2.withdraw(asset, sum, address, blockchain_2)
    elif send_point == 'invest' and destination_point == "futures":
        address = BINANCE_ADDRESSES[blockchain_2]

        futures_bal = float(mongo_db_futures_trading.get_balance(id))
        futures_bal += sum
        mongo_db_futures_trading.change_balance(id, futures_bal)
        bin_2.withdraw("USDT", sum, address, blockchain_1)
        prev_balance = curr_balance = float(bin.get_spot_balance(asset))
        while curr_balance <= prev_balance:
            time.sleep(60)
            curr_balance = float(bin.get_spot_balance(asset))
        bin.transfer_spot_to_futures(sum, "USDT")

    elif send_point == 'spot' and destination_point == 'spot':
        asset_from = data["asset_from"]
        asset_to = data["asset_to"]
        if asset_from != 'USDT':
            balance_from = bin.get_spot_balance('USDT')
            bin.open_spot_position(asset_from + 'USDT',
                                   'SELL', sum, 'MARKET', id)
            time.sleep(3)
            balance_to = bin.get_spot_balance('USDT')
            qty = (float(balance_to) - float(balance_from)) / float(bin.client.get_symbol_ticker(
                symbol=asset_to + 'USDT')['price']) * 0.99
        else:
            qty = float(sum) / float(bin.client.get_symbol_ticker(
                symbol=asset_to + 'USDT')['price']) * 0.99
        bin.open_spot_position(asset_to + 'USDT', 'BUY', qty, 'MARKET', id)
    elif send_point == 'wallet' and destination_point == 'wallet':
        asset_from = data["asset_from"]
        asset_to = data["asset_to"]
        os.system(
            f'python3 convert_wallet.py {id} {blockchain_1} {blockchain_2} {sum} {asset_from} {asset_to}')
    elif send_point == "pidar":
        bin_2.transfer_futures_to_spot(19.2, "USDT")

    return json.dumps({}), 200, {"ContentType": "application/json"}


@app.route("/close_all_futures_positons",  methods=["POST"])
@cross_origin()
def close_all_futures_positons():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])

    positions = mongo_db_futures_trading.get_positions(id)
    limit_positions = mongo_db_futures_trading.get_limit_positions(id)

    for pose in positions:
        coin_poses = positions[pose]
        if coin_poses["BUY"] != []:
            pair = pose
            side = "BUY"
            qnt = coin_poses["BUY"][1]
            leverage = coin_poses["BUY"][0]
            bin.close_part_of_open_position_market(
                pair, side, qnt, id, leverage)
        elif coin_poses["SELL"] != []:
            pair = pose
            side = "SELL"
            qnt = coin_poses["SELL"][1]
            leverage = coin_poses["SELL"][0]
            bin.close_part_of_open_position_market(
                pair, side, qnt, id, leverage)

    for pair in limit_positions:
        for side in limit_positions[pair]:
            for type in limit_positions[pair][side]:
                for order_id in limit_positions[pair][side][type]:
                    bin.cancel_open_futures_order(pair, order_id)

    mongo_db_futures_trading.terminate_all_limit_position(id)
    mongo_db_futures_trading.remove_all_positions(id)
    mongo_db_futures_trading.change_balance(id, 0)

    positions = mongo_db_futures_trading.get_positions(id)
    open_orders = mongo_db_futures_trading.get_limit_positions(id)
    balance = mongo_db_futures_trading.get_balance(id)

    return json.dumps({'positions': positions, "open_orders": open_orders, "balance": balance}), 200, {"ContentType": "application/json"}


@app.route("/close_one_futures_position",  methods=["POST"])
@cross_origin()
def close_one_futures_position():
    try:
        data = request.json()
    except:
        data = request.json

    id = int(data['UserId'])
    pair = data['pair']
    side = data['side']

    positions = mongo_db_futures_trading.get_positions(id)
    limit_positions = mongo_db_futures_trading.get_limit_positions(id)

    coin_poses = positions[pair]
    qnt = coin_poses[side][1]
    leverage = coin_poses[side][0]
    bin.close_part_of_open_position_market(
        pair, side, qnt, id, leverage)

    if side == "BUY":
        side = "SELL"
    else:
        side = "BUY"

    try:
        for type in limit_positions[pair][side]:
            if type == "STOP_MARKET" or type == "TAKE_PROFIT_MARKET":
                for order_id in limit_positions[pair][side][type]:
                    bin.cancel_open_futures_order(pair, order_id)
    except Exception:
        pass

    positions = mongo_db_futures_trading.get_positions(id)
    open_orders = mongo_db_futures_trading.get_limit_positions(id)
    balance = mongo_db_futures_trading.get_balance(id)

    return json.dumps({'positions': positions, "open_orders": open_orders, "balance": balance}), 200, {"ContentType": "application/json"}


@app.route("/min_open_price",  methods=["POST"])
@cross_origin()
def min_open_price():
    try:
        data = request.json()
    except:
        data = request.json

    pair = data['pair']

    QUANTITY_PRECISIONS = {}
    info = Client().futures_exchange_info()

    for symbol_info in info["symbols"]:
        QUANTITY_PRECISIONS[symbol_info["symbol"]
                            ] = symbol_info["quantityPrecision"]

    qnt = QUANTITY_PRECISIONS[pair]

    if qnt == 0:
        min_qnt = 1
    elif qnt == 1:
        min_qnt = 0.1
    elif qnt == 2:
        min_qnt = 0.01
    elif qnt == 3:
        min_qnt = 0.001

    key = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    data = requests.get(key)
    data = data.json()
    cur_price = float(data['price'])

    min_sum = cur_price * min_qnt
    if min_sum < 10:
        min_sum = 10

    return json.dumps({"min_sum": min_sum}), 200, {"ContentType": "application/json"}


@app.route("/")
@cross_origin()
def main():
    return "HI"
