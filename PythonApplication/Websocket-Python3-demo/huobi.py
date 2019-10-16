# -*- coding: utf-8 -*-
import json
import time
import gzip


from websocket import create_connection
from pprint import pprint
from PythonSqlite import GHuoBiSqlite

# 订阅 KLine 数据
tradeStr_kline = """
        {"sub": "market.BTC_CQ.kline.1min",  "id": "id1"}
        """

# 订阅 Market Detail 数据
tradeStr_marketDetail = """
        {"sub": "market.ETH_CW.detail",  "id": "id6" }
        """

# 订阅 Trade Detail 数据
tradeStr_tradeDetail = """
        {"sub": "market.ETH_CW.trade.detail", "id": "id7"}
        """

# 请求 KLine 数据
tradeStr_klinereq = """
        {"req": "market.BTC_CQ.kline.1min", "id": "id4"}
        """

# 请求 Trade Detail 数据
tradeStr_tradeDetail_req = """
        {"req": "market.BTC_CQ.trade.detail", "id": "id5"}
        """

# 订阅 Market Depth 数据
tradeStr_marketDepth = """
        {
            "sub": "market.BTC_CQ.depth.step0", "id": "id9"
        }
        """

GDataBase = []
class HuoBiDingYueData:
    amount = 0
    direction = ''
    price = 0.0
    ts = ''

class HuoBiDingYue:
    __ws__ = ''
    __trade_id = ''

    #链接服务器
    def Connect(self):
        try:
            self.__ws__ = create_connection("wss://www.hbdm.com/ws", http_proxy_host='127.0.0.1', http_proxy_port='1080')
            self.__ws__.send(tradeStr_tradeDetail)
            pprint('connect ws Success')
            return 1
        except:
            print('connect ws error')
            return 0

    #接受订阅信息
    def tick(self):
        compressData = self.__ws__.recv()
        result = gzip.decompress(compressData).decode('utf-8')

        # 是否是心跳
        if result[:7] == '{"ping"':
            pprint('Receive ping')
            ts = result[8:21]
            pong = '{"pong":' + ts + '}'
            self.__ws__.send(pong)
            pprint('Send pong')
            # ws.send(tradeStr_marketDetail)
        else:
            try:
                jsonValue = json.loads(result)
                #打印结果
                pprint(jsonValue)
                tempId = jsonValue['tick']['id']

                if self.__trade_id == tempId:
                    print('重复的id')
                    return
                else:
                    trade_id = tempId

                    for index in range(100):
                        try:
                            tempData = jsonValue['tick']['data'][index]
                            tempinfo = HuoBiDingYueData()
                            tempinfo.amount = tempData['amount']
                            tempinfo.direction = tempData['direction']
                            tempinfo.price = tempData['price']
                            tempinfo.ts = tempData['ts']
                            GDataBase.append(tempData)
                            if len(GDataBase) > 10:
                                self.saveSqlite()
                                pass
                        except:
                            break

                    pprint('Receive New Order')

            except Exception:
                pprint('Receive Data Error')
                pass

    #保存数据库
    def saveSqlite(self):
        pprint('Save Sqlite Start')
        for var in GDataBase:
            pass

        GDataBase.clear()
        pprint('Save Sqlite End')
        pass



GHuoBiDingYue = HuoBiDingYue()