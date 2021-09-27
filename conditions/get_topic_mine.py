
import websocket
from threading import Thread
import time
import ssl
from common.log import log


class GetTopic:

    def __init__(self,url,content):
        self.url = url
        self.content = content

    # 定义一个用来接收监听数据的方法
    def on_message(self,ws, message):
        log.info("监听到服务器返回的消息,内容如下：")
        log.info(message)

    # 定义一个用来处理错误的方法
    def on_error(self,ws, error):
        log.info("-----连接出现异常，异常信息如下-----")
        log.info(error)

    # 定义一个用来处理关闭连接的方法
    def on_close(self,ws):
        log.info("-------连接已关闭------")

    def on_open(self,ws):
        def run(*args):
            for i in range(3):
                ws.send(self.content)
                time.sleep(1)

            time.sleep(1)
            ws.close()
            print("Thread terminating...")

        Thread(target=run).start()

    def run(self):
        ws = websocket.WebSocketApp(self.url,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


if __name__ == '__main__':
    ws = GetTopic(url="ws://ws2.quote-dev-1.bybit.com/realtime",content=
             '{"op": "subscribe", "args": ["candle.D.BTCUSD"]}')
    print(1111)
    ws.run()


