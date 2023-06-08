import uuid
import json
import binance
import websocket
from mongo_db_futures_trading import *
import traceback
import keys


class BinanceOrderListener:
    def __init__(self):
        print(0)
        self.ws = None
        self.start_listener()

    def start_listener(self):
        print("Restarting...")
        if self.ws:
            self.ws.close()
        print("Stopped expired listener.")
        self.client = binance.Client(keys.key, keys.secret)
        print("Initialized a client.")
        listen_key = self.client.futures_stream_get_listen_key()
        print("New listen key:", listen_key)
        socket = f"wss://fstream.binance.com/ws/{listen_key}"
        self.ws = websocket.WebSocketApp(socket, on_open=lambda ws: self.on_open(ws), on_close=lambda ws: self.on_close(ws),
                                         on_message=lambda ws, message: self.on_message(ws, message))
        self.ws.run_forever()

    def get_user_id_from_client_order_id(self, client_order_id):
        return int(client_order_id[:6])

    def calculate_margin(self, entry, qnt, lev):
        print((float(entry) * float(qnt))/float(lev))
        return (float(entry) * float(qnt))/float(lev)

    def calculate_pnl(self, margin, exit_price, entry_price, lev, side):
        res = (exit_price / (entry_price / 100))
        if side == "SELL":
            return margin * (((100 - res) * lev) * 0.01)
        return margin * (((res - 100) * lev) * 0.01)


    def calculate_liq_price(self, leverage, cur_price, side, isol_cross, balance=0, margin=0):
        leverage = float(leverage)
        cur_price = float(cur_price)
        if isol_cross == "ISOLATED":
            if side == "SELL":
                res = cur_price + cur_price * ((95 / leverage) / 100)
                return float(round(res, 7))
            else:
                res = cur_price - cur_price * ((95 / leverage) / 100)
                return float(round(res, 7))

        else:
            cross = balance / margin
            if side == "SELL":
                res = cur_price + cur_price * (((100 / leverage) / 100) * cross)
                return float(round(res, 7))
            else:
                res = cur_price - cur_price * \
                    (((100 / leverage) / 100) * cross)
                return float(round(res, 7))

    def open_futures_liquidation_position(self, SYMBOL, SIDE, QTY, PRICE, id, leverage, isol_cros):
        if SIDE == "BUY":
            side_for_order = "SELL"
            positionSide = "LONG"
        else:
            side_for_order = "BUY"
            positionSide = "SHORT"
        self.client.futures_create_order(symbol=SYMBOL,
                                         side=side_for_order,
                                         positionSide=positionSide,
                                         type='STOP_MARKET',
                                         timeInForce='GTC',
                                         quantity=QTY,
                                         stopPrice=PRICE,
                                         newClientOrderId=self.generate_client_order_id(
                                             id, leverage, isol_cros, True),
                                         workingType='MARK_PRICE'
                                         )

    def generate_client_order_id(self, user_id, leverage, isol_cross, liq=False):
        order_id = str(uuid.uuid4())
        user_id_str = str(user_id)
        user_id_str = "0" * (6 - len(user_id_str)) + user_id_str
        user_lev_str = str(leverage)
        user_lev_str = "0" * (6 - len(user_lev_str)) + user_lev_str
        order_id = user_id_str + user_lev_str + order_id[12:]
        if isol_cross == "ISOLATED":
            order_id = order_id[:13] + \
                "0" + order_id[14:]
        else:
            order_id = order_id[:13] + \
                "1" + order_id[14:]
        if liq:
            order_id = order_id[:15] + \
                "0" + order_id[16:]
        else:
            order_id = order_id[:15] + \
                "1" + order_id[16:]
        return order_id

    def get_user_lev_from_client_order_id(self, client_order_id):
        return int(client_order_id[6:12])

    def get_user_liq_info_from_client_order_id(self, client_order_id):
        if client_order_id[15] == '0':
            return True
        return False

    def get_user_position_type_from_client_order_id(self, client_order_id):
        if client_order_id[13] == '0':
            return "ISOLATED"
        else:
            return 'CROS'

    def on_open(self, ws):
        print("Opened connection to Binance streams")

    def on_close(self, ws):
        print("Closed connection to Binance streams")

    def cancel_open_futures_order(self, SYMBOL, clientOrderId):
        self.client.futures_cancel_order(symbol=SYMBOL,
                                         origClientOrderId=clientOrderId)

    def on_message(self, ws, message):
        try:
            print("Message received from Binance streams")
            json_message = json.loads(message)
            print(json_message)
            if json_message["e"] == "listenKeyExpired":
                self.start_listener()

            elif json_message["e"] == "ORDER_TRADE_UPDATE":
                pair = json_message['o']['s']
                client_order_id = json_message['o']['c']
                id = self.get_user_id_from_client_order_id(client_order_id)
                lev = self.get_user_lev_from_client_order_id(client_order_id)
                isol_cros = self.get_user_position_type_from_client_order_id(
                    client_order_id)
                qnt = json_message['o']['q']
                entry_price = json_message['o']['ap']
                side = json_message['o']['S']
                position_side = json_message['o']['ps']

                # if self.get_user_liq_info_from_client_order_id(client_order_id):
                #     entry_price = json_message['o']['sp']
                #     add_new_limit_position(
                #         id, client_order_id, pair, lev, entry_price, qnt, side, "LIQUIDATION")
                #     print("LIQ_NEW")

                if json_message['o']['o'] == "MARKET" and json_message["o"]["X"] == "FILLED":
                    if side == "BUY" and position_side == "LONG":
                        if pair not in get_positions(id, pair) or get_positions(id, pair)[pair][side] == []:
                            add_new_position(
                                id, pair, lev, qnt, entry_price, side, isol_cros)
                            # liq_price = self.calculate_liq_price(lev, entry_price, side, self.get_user_position_type_from_client_order_id(
                            #     client_order_id), get_balance(id), self.calculate_margin(entry_price, qnt, lev))

                            # self.open_futures_liquidation_position(
                            #     pair, side, qnt, liq_price, id, lev, isol_cros)

                        else:
                            pose = get_positions(id, pair)[pair][side]
                            remove_position(id, side, pair)
                            new_qnt = float(pose[1]) + float(qnt)
                            new_entry_price = (
                                float(pose[2]) + float(entry_price)) / 2
                            # if side == "BUY":
                            #     side = "SELL"
                            # else:
                            #     side = "BUY"
                            # remove_limit_position(
                            #     id, client_order_id, pair, 'LIQUIDATION', side)
                            # if side == "BUY":
                            #     side = "SELL"
                            # else:
                            #     side = "BUY"
                            # liq_price = self.calculate_liq_price(lev, new_entry_price, side, self.get_user_position_type_from_client_order_id(
                            #     client_order_id), get_balance(id), self.calculate_margin(new_entry_price, new_qnt, lev))
                            # print('liq', liq_price)

                            # self.open_futures_liquidation_position(
                            #     pair, side, new_qnt, liq_price, id, lev, isol_cros)

                            add_new_position(id, pair, lev, str(
                                new_qnt), str(new_entry_price), side, isol_cros)
                        margin = self.calculate_margin(entry_price, qnt, lev)
                        cur_dep = get_balance(id)
                        change_balance(id, cur_dep - margin)
                    elif side == "SELL" and position_side == "LONG":
                        side = "BUY"
                        pose = get_positions(id, pair)[pair][side]
                        remove_position(id, side, pair)
                        if float(pose[2]) != 0:
                            pnl = self.calculate_pnl(
                                (float(pose[1]) * float(pose[2]))/lev, float(entry_price), float(pose[2]), lev, side)
                            user_dep = get_balance(id)
                            change_balance(id, user_dep + pnl)
                        new_qnt = float(pose[1]) - float(qnt)
                        if new_qnt > 0:
                            add_new_position(id, pair, lev, str(
                                new_qnt), entry_price, side, isol_cros)
                        margin = self.calculate_margin(entry_price, qnt, lev)
                        cur_dep = get_balance(id)
                        change_balance(id, cur_dep + margin)

                    elif side == "SELL" and position_side == "SHORT":
                        print("SELL_SHORT")
                        if pair not in get_positions(id, pair) or get_positions(id, pair)[pair][side] == []:
                            add_new_position(
                                id, pair, lev, qnt, entry_price, side, isol_cros)
                        else:
                            pose = get_positions(id, pair)[pair][side]
                            remove_position(id, side, pair)
                            new_qnt = float(pose[1]) + float(qnt)
                            new_entry_price = (
                                float(pose[2]) + float(entry_price)) / 2
                            add_new_position(id, pair, lev, str(new_qnt),
                                             str(new_entry_price), side, isol_cros)
                        margin = self.calculate_margin(entry_price, qnt, lev)
                        cur_dep = get_balance(id)
                        change_balance(id, cur_dep - margin)
                    elif side == "BUY" and position_side == "SHORT":
                        side = "SELL"
                        pose = get_positions(id, pair)[pair][side]
                        remove_position(id, side, pair)
                        if float(pose[2]) != 0:
                            pnl = self.calculate_pnl(
                                (float(pose[1]) * float(pose[2]))/lev, float(entry_price), float(pose[2]), lev, side)
                            user_dep = get_balance(id)
                            change_balance(id, user_dep + pnl)
                        new_qnt = float(pose[1]) - float(qnt)
                        if new_qnt > 0:
                            add_new_position(
                                id, pair, lev, str(new_qnt), entry_price, side, isol_cros)
                        margin = self.calculate_margin(entry_price, qnt, lev)
                        cur_dep = get_balance(id)
                        change_balance(id, cur_dep + margin)

                elif json_message['o']['o'] == "LIMIT" and json_message["o"]["X"] == "NEW":
                    entry_price = json_message['o']['sp']
                    add_new_limit_position(
                        id, client_order_id, pair, lev, entry_price, qnt, side, "LIMIT", isol_cros)
                    margin = self.calculate_margin(entry_price, qnt, lev)
                    cur_dep = get_balance(id)
                    change_balance(id, cur_dep - margin)
                    print("LIMIT_NEW")

                elif json_message['o']['o'] == "LIMIT" and json_message["o"]["X"] == "CANCELED":
                    entry_price = json_message['o']['sp']
                    remove_limit_position(
                        id, client_order_id, pair, "LIMIT", side)
                    print("LIMIT_CANCELED")
                    margin = self.calculate_margin(entry_price, qnt, lev)
                    cur_dep = get_balance(id)
                    change_balance(id, cur_dep + margin)

                elif json_message['o']['o'] == 'TAKE_PROFIT_MARKET' and json_message["o"]["X"] == "CANCELED":
                    remove_limit_position(
                        id, client_order_id, pair, 'TAKE_PROFIT_MARKET', side)
                    print("LIMIT_TAKE_CANCELED")

                elif json_message['o']['o'] == 'STOP_MARKET' and json_message["o"]["X"] == "CANCELED":
                    remove_limit_position(
                        id, client_order_id, pair, 'STOP_MARKET', side)
                    print("LIMIT_STOP_CANCELED")

                elif json_message['o']['o'] == "LIMIT" and json_message["o"]["X"] == "FILLED":
                    remove_limit_position(
                        id, client_order_id, pair, "LIMIT", side)

                    if side == "BUY" and position_side == "LONG":
                        print("limit_fill_buy_long")
                        if pair not in get_positions(id, pair) or get_positions(id, pair)[pair][side] == []:
                            add_new_position(
                                id, pair, lev, qnt, entry_price, side, isol_cros)
                        else:
                            pose = get_positions(id, pair)[pair][side]
                            remove_position(id, side, pair)
                            new_qnt = float(pose[1]) + float(qnt)
                            new_entry_price = (
                                float(pose[2]) + float(entry_price)) / 2
                            add_new_position(
                                id, pair, lev, str(new_qnt), str(new_entry_price), side, isol_cros)

                    elif side == "SELL" and position_side == "SHORT":
                        print("limit_fill_sell_dhort")
                        if pair not in get_positions(id, pair) or get_positions(id, pair)[pair][side] == []:
                            add_new_position(
                                id, pair, lev, qnt, entry_price, side, isol_cros)
                        else:
                            pose = get_positions(id, pair)[pair][side]
                            remove_position(id, side, pair)
                            new_qnt = float(pose[1]) + float(qnt)
                            new_entry_price = (
                                float(pose[2]) + float(entry_price)) / 2
                            add_new_position(id, pair, lev, str(new_qnt),
                                             str(new_entry_price), side, isol_cros)
                    margin = self.calculate_margin(entry_price, qnt, lev)
                    cur_dep = get_balance(id)
                    change_balance(id, cur_dep - margin)
                elif json_message['o']['o'] == "STOP_MARKET" and json_message["o"]["X"] == "NEW":
                    entry_price = json_message['o']['sp']
                    add_new_limit_position(
                        id, client_order_id, pair, lev, entry_price, qnt, side, "STOP_MARKET", isol_cros)
                    print("STOP_MARKET_NEW")
                elif json_message['o']['o'] == "TAKE_PROFIT_MARKET" and json_message["o"]["X"] == "NEW":
                    entry_price = json_message['o']['sp']
                    add_new_limit_position(
                        id, client_order_id, pair, lev, entry_price, qnt, side, "TAKE_PROFIT_MARKET", isol_cros)
                elif json_message['o']['o'] == "STOP_MARKET" and json_message["o"]["X"] == "EXPIRED":
                    pose = get_limit_positions(
                        id)[pair][side]["STOP_MARKET"][client_order_id]
                    remove_limit_position(
                        id, client_order_id, pair, "STOP_MARKET", side)

                    takes_to_remove = get_all_take_profits_for_pair(
                        id, pair, side)
                    for order_id in takes_to_remove:
                        self.cancel_open_futures_order(pair, order_id)

                    remove_position(id, side, pair)
                    new_qnt = float(pose[1]) - float(qnt)
                    if new_qnt > 0:
                        add_new_position(
                            id, pair, lev, str(new_qnt), entry_price, side, isol_cros)
                elif json_message['o']['o'] == "TAKE_PROFIT_MARKET" and json_message["o"]["X"] == "EXPIRED":
                    print("take_prof_fill")
                    pose = get_limit_positions(
                        id)[pair][side]["TAKE_PROFIT_MARKET"][client_order_id]
                    remove_limit_position(
                        id, client_order_id, pair, "TAKE_PROFIT_MARKET", side)

                    stops_to_remove = get_all_stop_losses_for_pair(
                        id, pair, side)
                    for order_id in stops_to_remove:
                        self.cancel_open_futures_order(pair, order_id)

                    remove_position(id, side, pair)
                    new_qnt = float(pose[1]) - float(qnt)
                    if new_qnt > 0:
                        add_new_position(
                            id, pair, lev, str(new_qnt), entry_price, side, isol_cros)
        except Exception as e:
            traceback.print_exc()


BinanceOrderListener()
