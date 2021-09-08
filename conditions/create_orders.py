
import requests

class GreateOrder:


    def logoin(self):
        url = "http://api2.quote-dev-1.bybit.com/"
        parameter = {"username": "seven.wu@yijinin.com",
                     "password": "8262202b763c9071281e137ee99f811dac75c237fa3042ae18124d7f93da6559",
                     "type": "recaptcha", "key_version": "v2",
                     "g_recaptcha_response": "03AGdBq27FInbaWbegejWM3ziD5z5iJCqz_lmUYieO4dP7aV2BS9SfdoeOe3KRObbZamLdxe3qKJZiae3OGkCIur01czQ4V038fi6rW6elSumIrdDbIupGcoTrECEidtv7RiJlHpc5rRGH2UBOLPs7JGh1MBjBP7Mh5dCk0xv8hPUIR0LNTf-_Znzg36nwI9SG-038JhBGyAFH5OsBgCQgzKuzkuAAENdxGaAGAtUhSxkOHg7g_LXACRdybOe7csizrGqU6hyEQB0V0fL62BoWVA4MzuBW6U1FudJHE4MBcImSomlmL1GJj-sbrk2CNM0D9bLy7Y3gXtIAUlGQrm1gVXYE156nqYSzQEzHTHBJALULRuxpFWXzwobwpR1uJu_UlWRoPMOhkWqkqNri72lm80ylq5yxEt8_W1AZXD9XN8gn-6LZT9yLXD9bFDc_0xnjAYtt2TTZ-v784TysIEm1CHMNNcYvIk8qiCMG3oWFUWPlB4EJF4lpGjwzyfc-jxHiOgI6dUeub_u8D7Whdv4mEkSr7Ul3iP6uFHEvRguvgDN9LG_ISZZObMn3maBxIkwF9qM-UDJ3sNZ35tVtYK1oUmYqziHMDhr1iV2SvWD-xS0EiKQJrhRjtgXGTQiYks099ArXoqYmMJjtpWT-jDe1vZl7lNV9RrsAH-UfFn8z1BR1x_bJh8YYMCmyFWkS8jhp4Zs-UtjKQsnbqWOP5sIccc1iCwZwfuuc2PcFrQS8KprskvIxxuhd8PE0OLMEUAa5-CWwNuZPi1L3jOuIgIWQn7-HwVknFUu_qFt0YBqkIHhyuvdCtUnTIaySRkI-_CUZpXLJ6HLyiPwoo0I3c9wnhLOHpI5G6u3CY2oMrl2nvvNGwYCkVE7sjqaQrV20OEqmzSLTYAHASfwrU7pBkhcT9j9wrnelYNOqb0pWICk715BHiVNQztyXJD0dwnftagQa3Z7S-PXeYpdq5StjCbN4Hdd8L7lF61dllapkrOZVGyP3lFy3nA-YDvrro355L9h46wC0T_5GJvwpZSCLD5icaCobxNZa3vtnXeNmJMCohvb38XdmGDyKVDTENmUhct-icuC3YNvfF7YAaMXrDK0dldVd-6jdkeAuTUhwaaCRO_uk1usFwqzJCv1cxwq7VRm1Pj744HSYR0Y54mqMGPCK-evY8O_n_M-ANnmD_1f0IbsE1VhgZ9SPi254ZBZH_1BECPrjR3GWblPm06hNOUB_CPM9nwEuZ4z6UF_sq6svtq5J0Jl914EdDIPo-h_w0WmEBXSr6BHM9yvd0V6rt-57v_d1nuMtSNnVoVFMmokhnUabtherTKFwicQRlXtK_71cMdSd8OUwkwhUEPRcW6damzN0Zy_tBN7f_7TdC-KLYzYEIMzpHiphDjWDitywjtDEnF442Rh9Lqur72OzgYPhuKk1lUi59Up58OzPUERhljb9VpW-epTQLHbbFWTnCLygI-7FVGFVB34CQdjnOH9ihI8CPllJip4FR_m75CEHJtlcPK1LctYdEG2sNwfA2qDPLTjfL7o_NtX-Agrog5_LvOszvHhv0Btk_dKYe-OIg5cWUrR5sMFJkM_jFi-tojLZhyiXWpdrPx4h"}
        rep = requests.post(url=url + "login", json=parameter)
        rep = rep.json()
        token = rep["token"]
        print(token)
        return token

    def create_order(self):
        token = self.logoin()
        url = "http://api2.quote-dev-1.bybit.com/private/linear/order/create"
        body = {"orderType":"Limit","side":"Buy","timeInForce":"GoodTillCancel","qty":100,"price":0.08743,"tpTriggerBy":"LastPrice","slTriggerBy":"LastPrice","reduceOnly":False,"leverage":10,"closeOnTrigger":False,"qty_type":1,"symbol":"TRXUSDT","basePrice":0.08743,"liqPrice":0.00001,"action":"Open"}
        headers = {"UserToken":token}
        rep = requests.post(url=url,json=body,headers=headers)
        print(rep.json())
        return rep.json()


if __name__ == '__main__':
    a = GreateOrder()
    a.create_order()