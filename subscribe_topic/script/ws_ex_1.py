import websocket
from threading import Thread
import time
import sys
import json

def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")



def on_open(ws):
    def run(*args):
        for i in range(3):
            ws.send('{"op": "subscribe", "args": ["candle.D.BTCUSD"]}')
            time.sleep(1)

        time.sleep(1)
        ws.close()
        print("Thread terminating...")
    Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    host = "ws://ws2.quote-dev-1.bybit.com/realtime"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    # print(ws.on_message)
    ws.on_open = on_open
    # recv_j = json.loads(recv)
    ws.run_forever()