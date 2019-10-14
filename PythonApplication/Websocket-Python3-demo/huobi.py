# -*- coding: utf-8 -*-
import json

from websocket import create_connection
import gzip
import time
from pprint import pprint

if __name__ == '__main__':
    while(1):
        try:
            ws = create_connection("wss://www.hbdm.com/ws", http_proxy_host='127.0.0.1', http_proxy_port='1080')
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    tradeStr_kline="""
    {"sub": "market.BTC_CQ.kline.1min",  "id": "id1"}
    """

    # 订阅 Market Detail 数据
    tradeStr_marketDetail="""
    {"sub": "market.ETH_CW.detail",  "id": "id6" }
    """

    # 订阅 Trade Detail 数据
    tradeStr_tradeDetail="""
    {"sub": "market.ETH_CW.trade.detail", "id": "id7"}
    """

    # 请求 KLine 数据
    tradeStr_klinereq="""
    {"req": "market.BTC_CQ.kline.1min", "id": "id4"}
    """

    # 请求 Trade Detail 数据
    tradeStr_tradeDetail_req="""
    {"req": "market.BTC_CQ.trade.detail", "id": "id5"}
    """

    # 订阅 Market Depth 数据
    tradeStr_marketDepth="""
    {
        "sub": "market.BTC_CQ.depth.step0", "id": "id9"
    }
    """

    #订阅成交记录
    ws.send(tradeStr_tradeDetail)
    trade_id = ''
    while(1):
        compressData=ws.recv()
        result=gzip.decompress(compressData).decode('utf-8')

        #是否是心跳
        if result[:7] == '{"ping"':
            pprint('Receive ping')
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
            pprint('Send pong')
            #ws.send(tradeStr_marketDetail)
        else:
            try:
                jsonValue = json.loads(result)
                pprint(jsonValue)
                tempId = jsonValue['tick']['id']

                if trade_id == tempId:
                    print('重复的id')
                    break
                else:
                    trade_id = tempId
                    pprint('Receive New Order')

            except Exception:
                pprint('Receive Data Error')
                pass
