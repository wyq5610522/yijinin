from confing.confing import create_order_path,base_bath
import sys
sys.path.append(base_bath)
import requests
from conditions.common.load_file import LoadFile


class GreateOrder:

    result = LoadFile(create_order_path).get_data()

    def __init__(self,url,user=None,volure=None):
        self.url = url
        self.user = user
        self.volure = volure

    def logoin(self):

        if self.user is None:
            user_data = self.result.get('user_1')
        else:
            user_data = self.result.get(self.user)
        rep = requests.post(url=self.url + "/login", json=user_data)
        rep = rep.json()
        token = rep.get("token")
        print(token)
        return token


    def by(self):
        token = self.logoin()
        path = self.result.get('order_path')
        url = self.url+path
        body = self.result.get("by")
        if self.volure:
            body['qtyX'] = str(self.volure)
        headers = {"UserToken":token}
        rep = requests.post(url=url,json=body,headers=headers)
        print(rep.json())
        return rep.json()

    def sell(self):
        token = self.logoin()
        path = self.result.get('order_path')
        url = self.url + path
        body = self.result.get("sell")
        if self.volure:
            body['qtyX'] = str(self.volure)
        headers = {"UserToken":token}
        rep = requests.post(url=url,json=body,headers=headers)
        print(rep.json())
        return rep.json()

if __name__ == '__main__':
    url = "http://api2.quote-dev-1.bybit.com"
    a = GreateOrder(url,user="user_1",volure=1)
    a.logoin()
    # b = GreateOrder(url, user="user_2", volure=1)
    # b.sell()