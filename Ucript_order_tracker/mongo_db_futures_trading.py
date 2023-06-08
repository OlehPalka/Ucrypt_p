import keys
from binance import Client
from pymongo import *
from keys import *
cluster = MongoClient(
    "...")
db = cluster["Ucript"]
futures_table = db["Futures_Trading"]
client = Client(keys.key, keys.secret)


def cancel_open_futures_order(SYMBOL, clientOrderId):
    client.futures_cancel_order(symbol=SYMBOL,
                                origClientOrderId=clientOrderId)


def add_new_client(id, email, balance=0, positions={}, limit_positions={}, PNL=0):
    futures_table.insert_one({
        "_id": id,
        "email": email,
        "balance": balance,
        "positions": positions,
        "limit_orders": limit_positions,
        "PNL": PNL
    })


def get_balance(id):
    return futures_table.find_one(id)["balance"]


def get_positions(id, pair=""):
    return futures_table.find_one(id)['positions']


def get_user_id_by_orderid(orderid):
    bd = futures_table.find({}, {'_id': 1, 'email': 1, 'balance': 1, 'positions': 1, "limit_orders": 1,
                                 "PNL": 1})
    for i in bd:
        print(i)
    return bd


def get_limit_positions(id):
    return futures_table.find_one(id)['limit_orders']


def get_pnl(id):
    return futures_table.find_one(id)["PNL"]


def change_balance(id, balance):
    futures_table.update_one({'_id': id}, {"$set": {
                             "balance": balance}})


def add_new_position(id, pair, leverage, position_size, entry_point, side, cros_lim):
    poses = get_positions(id, pair)
    if pair not in poses:
        poses[pair] = {"BUY": [],
                       "SELL": []}

    poses[pair][side] = [leverage, position_size,
                         entry_point, cros_lim]
    futures_table.update_one({'_id': id}, {"$set": {
                             "positions": poses}})


def remove_position(id, side: str, pair):
    poses = get_positions(id, pair)
    poses[pair][side] = []
    if poses[pair]["BUY"] == [] and poses[pair]["SELL"] == []:
        poses.pop(pair)
    futures_table.update_one({'_id': id}, {"$set": {
                             "positions": poses}})


def get_all_take_profits_for_pair(id, pair, side):
    poses = get_limit_positions(id)[pair][side]["TAKE_PROFIT_MARKET"]
    return poses


def get_all_stop_losses_for_pair(id, pair, side):
    poses = get_limit_positions(id)[pair][side]["STOP_MARKET"]
    return poses


def add_new_limit_position(id, client_order_id, pair, leverage, entry_point, position_size, side, type_or, cros_isol):
    poses = get_limit_positions(id)
    if pair not in poses:
        poses[pair] = {"BUY": {"LIMIT": {},
                               "STOP_MARKET": {},
                               "TAKE_PROFIT_MARKET": {},
                               "LIQUIDATION": {}},
                       "SELL": {"LIMIT": {},
                                "STOP_MARKET": {},
                                "TAKE_PROFIT_MARKET": {},
                                "LIQUIDATION": {}}}

    poses[pair][side][type_or][client_order_id] = [leverage, position_size,
                                                   entry_point, cros_isol]
    futures_table.update_one({'_id': id}, {"$set": {
                             "limit_orders": poses}})


def remove_limit_position(id, client_order_id: str, pair, type_or, side):
    poses = get_limit_positions(id)
    if type_or == "LIQUIDATION":
        print('liq_deleted')
        cancel_open_futures_order(pair, client_order_id)
        poses[pair][side][type_or] = {}
        futures_table.update_one({'_id': id}, {"$set": {
            "limit_orders": poses}})
    else:
        del poses[pair][side][type_or][client_order_id]
        futures_table.update_one({'_id': id}, {"$set": {
            "limit_orders": poses}})


def change_pnl(id, pnl):
    futures_table.update_one({'_id': id}, {"$set": {
                             "PNL": pnl}})


def delete_user(id):
    futures_table.delete_one({"_id": id})
