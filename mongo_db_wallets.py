from pymongo import *
cluster = MongoClient(
    "...")
db = cluster["Ucript"]
wallets_table = db["Wallets"]


def add_new_client(id, email, coins_adr=[], balance=0, different_adr_balance={}, pay_coin_balance=0, locked_coins_balance=0):
    wallets_table.insert_one({
        "_id": id,
        "email": email,
        "coins_adr": coins_adr,
        "balance": balance,
        "different_adr_balance": different_adr_balance,
        "pay_coin_balance": pay_coin_balance,
        "locked_coins_balance": locked_coins_balance
    })


def get_email(id):
    return wallets_table.find_one(id)["email"]


def get_balance(id):
    return wallets_table.find_one(id)["balance"]


def get_pay_coin_balance(id):
    return wallets_table.find_one(id)["pay_coin_balance"]


def get_coins_addresses(id):
    return wallets_table.find_one(id)["coins_adr"]


def get_different_addresses_balances(id):
    return wallets_table.find_one(id)["different_adr_balance"]


def get_locked_coins_balance(id):
    return wallets_table.find_one(id)["balance"]


def change_email(id, new_email):
    wallets_table.update_one({'_id': id}, {"$set": {
        "email": new_email}})


def change_balance(id, balance):
    wallets_table.update_one({'_id': id}, {"$set": {
        "balance": balance}})


def change_locked_coins_balance(id, balance):
    wallets_table.update_one({'_id': id}, {"$set": {
        "locked_coins_balance": balance}})


def change_pay_coin_balance(id, balance):
    wallets_table.update_one({'_id': id}, {"$set": {
        "pay_coin_balance": balance}})


def add_coin_adr(id, address):
    add = get_coins_addresses(id)
    add.append(address)
    wallets_table.update_one({'_id': id}, {"$set": {
        "coins_adr": add}})


def remove_coin_adr(id, address):
    add = get_coins_addresses(id)
    add.append(address)
    wallets_table.update_one({'_id': id}, {"$set": {
        "coins_adr": add}})


def set_address_balance(id, address, balance):
    add = get_different_addresses_balances(1)
    add[address] = balance
    wallets_table.update_one({'_id': id}, {"$set": {
        "different_adr_balance": add}})


def delete_user(id):
    wallets_table.delete_one({"_id": id})
