#!/usr/bin/python
# -*- coding: utf-8 -*
import ssl

import websocket
import time
import json
import _thread
# import logger
# import alarm_service
# import voiceclient
import jsonpath
import asyncio

def tools_fr(topic):
    topic_info = []
    if 'evaluate' in topic:
        topic = json.loads(topic[9:])
        for i in range(len(topic)):
            topic_info.append(json.dumps(topic[i]))
        return topic_info
    else:
        return topic

class Ws2_Monit():
    def __init__(self, topic, wait_time):
        websocket.enableTrace(True)
        self.topic = tools_fr(topic)
        self.wait_time = wait_time
        self.result = []
        self._message = []
        name = self.topic[0][-4]
        #判断正反向
        if name == "T":
            self.ws = websocket.WebSocketApp("wss://ws2.bybit.com/realtime_public",
                                             on_message=lambda ws, message: self.on_message(ws, message,'timestampE6'),
                                             on_error=lambda ws, error: self.on_error(ws, error),
                                             on_close=lambda ws: self.on_close(ws),
                                             on_open=lambda ws: self.on_open(ws)
                                             )
        else:
            self.ws = websocket.WebSocketApp("wss://ws2.bybit.com/realtime",
                                             on_message=lambda ws, message: self.on_message(ws, message,'timestamp_e6'),
                                             on_error=lambda ws, error: self.on_error(ws, error),
                                             on_close=lambda ws: self.on_close(ws),
                                             on_open=lambda ws: self.on_open(ws)
                                             )

    def on_message(self, ws, message, info):
        # log_file_name = 'index_quote_20-delay.log.' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # log = logger.Logger(log_file_name, level='info')
        # log.logger.info(message)
        self.result.append(message)
        # 对比所有接收到消息的本地和服务器时间戳，超过2s的标记为False
        if 'success' not in message and 'index_quote_20' in message:
            # 如果是合并包，取第一条做对比
            if type(json.loads(message)) == list:
                if int(time.time() * 1000000) - int((json.loads(message))[0][info]) < 2000000:
                    self._message.append(str(time.time()) + 'True')
                else:
                    # log.logger.info(message)
                    self._message.append(str(time.time()) + 'False')
            else:
                if int(time.time() * 1000000) - int(json.loads(message)[info]) < 2000000:
                    self._message.append(str(time.time()) + 'True')
                else:
                    # log.logger.info(message)
                    self._message.append(str(time.time()) + 'False')
        elif 'success' not in message and 'candle' in message:
            if int(time.time() * 1000000) - int(json.loads(message)[info]) < 2000000:
                self._message.append(str(time.time()) + 'True')
            else:
                # log_file_name = 'candle-delay.log.' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
                # log = logger.Logger(log_file_name, level='info')
                # log.logger.info(message)
                self._message.append(str(time.time()) + 'False')

    # 出现错误时执行
    def on_error(self, ws, error):
        print(error)

    # 关闭连接时执行
    def on_close(self, ws):
        print("websocket-closed")

    # 开始连接时执行：订阅对应topic，然后收一定时间的推送消息
    def on_open(self, ws):
        topiclist = self.topic
        timeinfo = self.wait_time
        def run(*args):
            for i in range(len(topiclist)):
                ws.send(topiclist[i])
            time.sleep(timeinfo)
            ws.close()

        _thread.start_new_thread(run, ())

    # 在线程停止时返回所有推送的数据
    def GetWebsocketData(self):
        # # 开启本地代理，方便调试
        # self.ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=1087,sslopt={"cert_reqs": ssl.CERT_NONE})
        # self.ws.run_forever(ping_interval=30, ping_timeout=5)
        print(self.result.__len__(), self._message)
        return self.result.__len__(), self.result, self._message

class Organization_Monit():
    def __init__(self, topic, wait_time):
        websocket.enableTrace(True)
        self.wait_time = int(wait_time)
        self.result = []
        self._message = []
        self.topic = tools_fr(topic)
        name =  self.topic[0][-4]
        if name == "T":
            self.ws = websocket.WebSocketApp("wss://stream.bybit.com/realtime_public",
                                             on_message=lambda ws, message: self.on_message(ws, message),
                                             on_error=lambda ws, error: self.on_error(ws, error),
                                             on_close=lambda ws: self.on_close(ws),
                                             on_open=lambda ws: self.on_open(ws)
                                             )
        else:
            self.ws = websocket.WebSocketApp("wss://stream.bybit.com/realtime",
                                             on_message=lambda ws, message: self.on_message(ws, message),
                                             on_error=lambda ws, error: self.on_error(ws, error),
                                             on_close=lambda ws: self.on_close(ws),
                                             on_open=lambda ws: self.on_open(ws)
                                             )

    def on_message(self, ws, message):
        # log_file_name = 'stream-delay.log.' + time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # log = logger.Logger(log_file_name, level='info')
        # log.logger.info(message)
        self.result.append(message)
        # 对比所有接收到消息的本地和服务器时间戳，超过2s的标记为False
        if 'success' not in message and 'orderBookL2_25' in message:
            if int(time.time() * 1000000) - json.loads(message)['timestamp_e6'] < 2000000:
                self._message.append(str(time.time()) + 'True')
            else:
                # log.logger.info(message)
                self._message.append(str(time.time()) + 'False')

    # 出现错误时执行
    def on_error(self, ws, error):
        print(error)

    # 关闭连接时执行
    def on_close(self, ws):
        print("websocket-closed")

    # 开始连接时执行：订阅对应topic，然后收一定时间的推送消息
    def on_open(self, ws):
        topiclist = self.topic
        timeinfo = self.wait_time
        def run(*args):
            for i in range(len(topiclist)):
                ws.send(topiclist[i])
            time.sleep(timeinfo)
            ws.close()

        _thread.start_new_thread(run, ())

    # 在线程停止时返回所有推送的数据
    def GetWebsocketData(self):
        # #开启本地代理，方便调试
        self.ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=1087, sslopt={"cert_reqs": ssl.CERT_NONE})
        # self.ws.run_forever(ping_interval=30,ping_timeout=5)
        return self.result.__len__(), self.result, self._message

if __name__ == '__main__':
    Ws2_Monit(['{"op":"subscribe","args":["trade.BTCUSD"]}',
                 '{"op":"subscribe","args":["trade.XRPUSD"]}'], 3).GetWebsocketData()
    # Organization_Monit(['{"op": "subscribe", "args": ["klineV2.1.BTCUSD"]}',
    #                '{"op": "subscribe", "args": ["trade.BTCUSD"]}','{"op": "subscribe", "args": ["klineV2.1.BTCUSD"]}'], 3).GetWebsocketData()
