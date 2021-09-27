#!/usr/bin/python
# -*- coding: utf-8 -*
import ssl

import websocket
import time
import json
import _thread
from common.log import log
from common.load_file import LoadFile
from confing.confing import public_topic_path


class Exchange_ws():
    def __init__(self, url, topic, wait_time):
        websocket.enableTrace(True)
        self.url = url
        self.wait_time = wait_time
        self.result = []
        self._message = []
        # self.token=Kucoin_http().getToken()
        self.topic = topic

        self.ws = websocket.WebSocketApp(url=self.url,
                                         on_message=lambda ws, message: self.on_message(ws, message),
                                         on_error=lambda ws, error: self.on_error(ws, error),
                                         on_close=lambda ws: self.on_close(ws),
                                         on_open=lambda ws: self.on_open(ws)
                                         )

    def on_message(self, ws, message):
        log.info(message)

    # 出现错误时执行
    def on_error(self, ws, error):
        log.info(error)

    # 关闭连接时执行
    def on_close(self, ws):
        log.info("websocket-closed")

    # 开始连接时执行：订阅对应topic，然后收一定时间的推送消息
    def on_open(self, ws):
        topic = self.topic
        timeinfo = self.wait_time

        def run(*args):
            log.info("开始订阅topic{}".format(topic))
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

    result = LoadFile(public_topic_path).get_data()
    print(result)
    # url = result["USDT_Petperual"]["testnet"]
    # time_sleep = 3
    # for topic  in  result["USDT_Petperual"]["topic"]:
    #     Exchange_ws(url,topic,time_sleep).GetWebsocketData()

    # Exchange_ws("wss://stream-testnet.bybit.com/realtime_public",
    #             '{"op":"subscribe","args":["candle.D.BTCUSDT"]}',
    #             3).GetWebsocketData()

    for noun in result["NOUN"]:
        topic = '{"op":"subscribe","args":["candle.D.BTCUSDT"]}'.replace("BTC", noun)
        print(topic)
        Exchange_ws("wss://stream-testnet.bybit.com/realtime_public",
                    topic,
                    3).GetWebsocketData()
