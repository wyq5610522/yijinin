# -*- encoding:utf-8 -*-

import gzip
import json
import random
import threading
import time
import zlib
from threading import Timer

import websocket
from gevent._semaphore import Semaphore
from locust import TaskSet, task, Locust, events

# TODO: 设置集合点...
all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()


events.hatch_complete += on_hatch_complete

t2 = 0
repCount = 0
sendCount = 0
pingCount = 0
stSend = 0
openTime = 0
reqLen = 0
recordSt = 0
repList = []
printCount = 1
reqSentCount = 1

symbols = ["etcusdt"]

subbedCount = 0
retSubTopicCount = 0
testFlag = 0


def on_message(ws, message):
    global t2
    global repCount
    global sendCount
    global pingCount
    global stSend
    global printCount
    global reqList
    global recordSt
    global subbedCount
    global retSubTopicCount
    global reqSentCount

    req_list = {

        "req_str1": '{"req": "market.%s.kline.1min"}' % random.choice(symbols),
        "req_str2": '{"req": "market.%s.depth.step0"}' % random.choice(symbols),
        "req_str3": '{"req": "market.%s.trade.detail"}' % random.choice(symbols),
        "req_str4": '{"req": "market.%s.detail"}' % random.choice(symbols),
        # "req_str5": '{"req": "market.overview"}',

    }

    # 对返回来的压缩数据进行解压缩
    ws_result = zlib.decompressobj(31).decompress(message)

    result = json.loads(ws_result.decode('utf-8'))
    print(result)

    recordEd = time.time()  # 为了判断什么时候统计数据的结束时间

    recordCost = round((recordEd - recordSt) * 1000, 3)  # 统计的结束时间减去统计的开始时间

    # print(result)

    if 'subbed' in result:

        subbedCount = subbedCount + 1

        if subbedCount % 5 == 0:
            print("----------------subbed all topic----------------")

    if 'ch' in result:
        retSubTopicCount = retSubTopicCount + 1

    if 'rep' in result:
        repCount = repCount + 1

        repRetTime = int((time.time() - stSend) * 1000)

        repList.append(repRetTime)

        # print("the server rep time is ---->%dms" % repRetTime)

        # print("the server rep data is ---->%s" % result)

    # 判断ping的返回 ，对应给服务器发送pong
    if 'ping' in result:
        pingCount = pingCount + 1
        ping_id = result.get('ping')
        pong_str = '{"pong": %d}' % ping_id
        ws.send(pong_str)

        t1 = ping_id

        t3 = ping_id - t2

        t2 = t1

        if t3 > 5000:
            print("$$$$$$$time difference ping is %d$$$$$$$ " % t3)

        # print("ret ping value %d" % ping_id)
        # print("ret ping curTime %d" % int(time.time()*1000))
        # if 1000 < int((time.time()*1000) - ping_id):
        #     print("cur - pingTime is  ---> %dms" % int((time.time()*1000) - ping_id))

    if recordCost >= (random.randint(2000, 3000) * reqSentCount):
        reqSentCount += 1
        for key in req_list.keys():
            ws.send(req_list[key])

            sendCount = sendCount + 1

            # print("send  req info is --------->", req_list[key])

            stSend = time.time()

        # print("**********send count is %d   *************** " % sendCount)

    # 每1分钟统计一次
    if recordCost >= (60000 * printCount):
        printCount = printCount + 1

        curTime = time.strftime('%Y-%m-%d %H:%M:%S')

        repList.sort()

        retCount = len(repList)

        writeData = '| 当前时间%s ,req发送条数%s,返回总数据条数%s |  数据95耗时:%s  | 数据50耗时:%s  | sub返回量:%s ' % (
            curTime, sendCount, repCount, repList[int(retCount * 0.95)], repList[int(retCount * 0.5)], retSubTopicCount)

        fid = open("GipRecord.txt", "a+")

        fid.write(writeData + "\n")

        fid.close()


# 重新实现对应事件
def on_error(ws, error):
    print("occur error " + error)


def on_close(ws):
    global printCount
    global reqSentCount
    printCount = 1
    reqSentCount = 1
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^con is closed^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


def on_open(ws):
    print("con success ...")
    global reqList
    global sendCount
    global reqLen
    global recordSt
    global stSend

    recordSt = time.time()  # 为了统计记录文件创建的开始时间

    stSend = time.time()

    sub_list = {

        "sub_str1": '{"sub": "market.%s.kline.1min"}' % random.choice(symbols),
        "sub_str2": '{"sub": "market.%s.depth.step0"}' % random.choice(symbols),
        "sub_str3": '{"sub": "market.%s.trade.detail"}' % random.choice(symbols),
        "sub_str4": '{"sub": "market.%s.detail"}' % random.choice(symbols),
        "sub_str5": '{"sub": "market.overview"}',

    }

    for key in sub_list.keys():
        ws.send(sub_list[key])


class WSClient(object):

    def __init__(self, host):
        self.ws = None
        self.host = host

    def useWebCreate(self):
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.host,
                                         # header={'cloud-exchange':'510a02991'},
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close,
                                         on_open=on_open)

    def execute(self):
        self.ws.run_forever()


class AbstractLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(AbstractLocust, self).__init__(*args, **kwargs)
        self.client = WSClient(self.host)


class ApiUser(AbstractLocust):
    host = 'ws://xxx/ws'

    min_wait = 10
    max_wait = 1000

    class task_set(TaskSet):
        def on_start(self):
            self.client.useWebCreate()
            # TODO: 设置集合点...
            all_locusts_spawned.wait()

        @task
        def execute_long_run(self):
            self.client.execute()