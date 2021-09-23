

import requests

url = "https://testnet.bybit.com/v2/public/account-ratio"


res = requests.get(url = url)
# res = res.json()
print(type(res.text))
print(res.text)