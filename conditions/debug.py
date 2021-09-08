#!/usr/bin/python
# -*- coding: utf-8 -*
import ssl

import websocket
import time
import json
import _thread
from log import Logger
import jsonpath
import asyncio

# from tools_http import Kucoin_http

class Exchange_ws():
    def __init__(self, topic, wait_time):
        websocket.enableTrace(True)
        self.wait_time = wait_time
        self.result = []
        self._message = []
        # self.token=Kucoin_http().getToken()
        self.topic=topic

        self.ws = websocket.WebSocketApp("ws://ws2.quote-dev-1.bybit.com/realtime",
                                         on_message=lambda ws, message: self.on_message(ws, message, 'timestampE6'),
                                         on_error=lambda ws, error: self.on_error(ws, error),
                                         on_close=lambda ws: self.on_close(ws),
                                         on_open=lambda ws: self.on_open(ws)
                                         )


    def on_message(self, ws, message, info):
        log_file_name = 'index_quote_20-delay.log.' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        log = Logger(log_file_name, level='info')
        log.logger.info(message)

    # 出现错误时执行
    def on_error(self, ws, error):
        print(error)

    # 关闭连接时执行
    def on_close(self, ws):
        print("websocket-closed")

    # 开始连接时执行：订阅对应topic，然后收一定时间的推送消息
    def on_open(self, ws):
        topic = self.topic
        timeinfo = self.wait_time
        def run(*args):
            ws.send(topic)
            time.sleep(timeinfo)
            ws.close()
        _thread.start_new_thread(run, ())
    # 在线程停止时返回所有推送的数据
    def GetWebsocketData(self):
        # 开启本地代理，方便调试
        # self.ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=1087,sslopt={"cert_reqs": ssl.CERT_NONE})
        # self.ws.run_forever(ping_interval=30, ping_timeout=5)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        print(self.result.__len__(), self._message)
        return self.result.__len__(), self.result, self._message

if __name__ == '__main__':
    Exchange_ws('{"op": "subscribe", "args": ["instrument_info.all"]}',
                3).GetWebsocketData()
    # Exchange_ws('{"id": 1545910660739,"type": "subscribe","topic": "/market/match:BTC-USDT","response": true}', 3).GetWebsocketData()
    # Exchange_ws({'kucoin':'{"id": 1545910660739,"type": "subscribe","topic": "/market/match:BTC-USDT","response": true}',
    #              'bitfinex':'{"event": "subscribe","channel": "trades","symbol": "SOLUSD"}'},
    #             5).GetWebsocketData()