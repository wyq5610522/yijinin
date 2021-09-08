from BybitWebsocket import BybitWebsocket


ws = BybitWebsocket(wsURL="wss://ws2.quote-dev-1.bybit.com/realtime",
                    api_key=None, api_secret=None)
ws.subscribe_instrument_info(symbol="BTCUSD")
ws.ws.send('{"op": "subscribe", "args": ["instrument_info.100ms.BTCUSD"]}')


while True:
    data = ws.get_data("instrument_info.100ms.BTCUSD")
    if data:
        print(data)


