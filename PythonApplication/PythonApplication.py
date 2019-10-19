import os
import sys
import time
import datetime
import xlrd
import json
import threading
from pprint import pprint


#数据结构
#import PythonThread
from HuobiData import GDataDMInfo, GDataGlobal, GDataDMBBInfo, Datacontract_index, GDataDMAllOrders, DataDMAllOrder

#QT
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
#QT UI
import PythonApplicationUI

#huoBi API
from HuobiDMService import HuobiDM


'''
======================
公用属性
======================
'''
GUsdt = 7.12


'''
======================
公用函数
======================
'''
# 保留4位小数
def convert2f(floatValue, nums=4):
    if floatValue:
        if nums == 0:
            return int(floatValue)
        else:
            return round(floatValue, nums)
    return 0.0




'''
======================
主页面类
======================
'''
class MuMainWindow(QMainWindow):
    '''
    ======================
    类函数API
    ======================
    '''
    def __init__(self):
        QMainWindow.__init__(self)

        #初始化UI
        self.__Slate = PythonApplicationUI.Ui_MainWindow()
        self.__Slate.setupUi(self)
        self.__Slate.BTNEOS.clicked.connect(self.CallEOSInfo)
        self.__Slate.BTNETH.clicked.connect(self.CallETHInfo)

        #初始化Key
        URL = ''
        ACCESS_KEY = ''
        SECRET_KEY = ''

        #读取key
        with open('C:\HuoBiKey.json', 'r') as loadf:
            load_dict = json.load(loadf)
            URL = load_dict['URL']
            ACCESS_KEY = load_dict['Access_Key']
            SECRET_KEY = load_dict['Secret_Key']

        # 初始化火币账号
        self.__HBAPI = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)

        #开启多线程
        self.__ApiThread = threading.Thread(target=self.ThreadUpdate)
        self.__ApiThread.daemon = 1
        self.__ApiThread.start()



    #定时更新线程
    def ThreadUpdate(self):
        delayTime = 1

        while 1:
            if GDataGlobal.GCurSymbol:
                #初始化,币基础信息,只刷新一次
                if GDataGlobal.GThreadFrames == 0:
                    self.CallContract_info()
                    pprint('刷新合约信息 ： {}'.format(GDataDMInfo.status))

                #2秒更新指数信息
                if GDataGlobal.GThreadFrames % 2 == 0:
                    self.Callcontract_index()

                # 5秒更新一次当前账户信息
                if GDataGlobal.GThreadFrames % 5 == 0:
                    self.Callcontract_account_info()
                    self.UpdateUIBBInfo()
                    # 输出当前属性
                    #GDataDMBBInfo.printObj()
                    pprint('刷新用户状态 ： {}'.format(GDataDMBBInfo.status))

                #5秒更新一次订单信息
                if GDataGlobal.GThreadFrames % 2 == 0:
                    self.callcontract_AllOrders()
                    self.updateOrdersInfo()
                    pprint('刷新所有订单状态 ： {}'.format(GDataDMAllOrders.status))

                GDataGlobal.GThreadFrames += delayTime

             #delay1秒钟
            time.sleep(delayTime)

    #查看某个币种
    def CallSeeBBInfo(self,symbol):
        GDataGlobal.GCurSymbol =symbol
        GDataGlobal.GThreadFrames = 0

    #当前状态是否有效
    def isAlready(self):
        return GDataGlobal.GCurSymbol
    '''
    ======================
    火币信息API
    ======================
    '''
    #获取合约信息
    def CallContract_info(self):
        if not self.isAlready():
            return

        try:
            jsonValue = self.__HBAPI.get_contract_info(GDataGlobal.GCurSymbol, 'this_week')
            GDataDMInfo.status = jsonValue['status']
            GDataDMInfo.symbol = jsonValue['data'][0]['symbol']
            GDataDMInfo.contract_code = jsonValue['data'][0]['contract_code']
            GDataDMInfo.contract_type = jsonValue['data'][0]['contract_type']
            GDataDMInfo.contract_size = jsonValue['data'][0]['contract_size']
            GDataDMInfo.price_tick = jsonValue['data'][0]['price_tick']
            GDataDMInfo.delivery_date = jsonValue['data'][0]['delivery_date']
            GDataDMInfo.create_date = jsonValue['data'][0]['create_date']
            GDataDMInfo.contract_status = jsonValue['data'][0]['contract_status']
            # GDataDMInfo.printObj()
        except Exception as e:
            GDataDMInfo.status = 'error'
            pprint(e)


    #获取账户信息
    def Callcontract_account_info(self):
        if not self.isAlready():
            return

        try:
            jsonValue = self.__HBAPI.get_contract_account_info(GDataGlobal.GCurSymbol)
            GDataDMBBInfo.status = jsonValue['status']
            GDataDMBBInfo.symbol = jsonValue['data'][0]['symbol']
            GDataDMBBInfo.margin_balance = jsonValue['data'][0]['margin_balance']
            GDataDMBBInfo.margin_position = jsonValue['data'][0]['margin_position']
            GDataDMBBInfo.margin_frozen = jsonValue['data'][0]['margin_frozen']
            GDataDMBBInfo.margin_available = jsonValue['data'][0]['margin_available']
            GDataDMBBInfo.profit_real = jsonValue['data'][0]['profit_real']
            GDataDMBBInfo.profit_unreal = jsonValue['data'][0]['profit_unreal']
            GDataDMBBInfo.risk_rate = jsonValue['data'][0]['risk_rate']
            GDataDMBBInfo.liquidation_price = jsonValue['data'][0]['liquidation_price']
            GDataDMBBInfo.withdraw_available = jsonValue['data'][0]['withdraw_available']
            GDataDMBBInfo.lever_rate = jsonValue['data'][0]['lever_rate']
            GDataDMBBInfo.adjust_factor = jsonValue['data'][0]['adjust_factor']
        except Exception as e:
            GDataDMBBInfo.status = 'error'
            pprint(e)


    #获取合约指数信息
    def Callcontract_index(self):
        if not self.isAlready():
            return

        try:
            jsonValue = self.__HBAPI.get_contract_index(GDataGlobal.GCurSymbol)
            if jsonValue['status'] == 'ok':
                GDataGlobal.Gindex_price = convert2f(jsonValue['data'][0]['index_price'])
            # GDataGlobal.printObj()
        except Exception as e:
            pprint(e)

    #获取当前币种持仓信息
    def callcontract_AllOrders(self):
        if not self.isAlready():
            return
        try:
            jsonValue = self.__HBAPI.get_contract_position_info(GDataGlobal.GCurSymbol)
            GDataDMAllOrders.status = jsonValue['status']

            if jsonValue['status'] == 'ok':
                #先清空
                GDataDMAllOrders.data.clear()
                nums = len(jsonValue['data'])
                for index in range(nums):
                    tempOrder = DataDMAllOrder()
                    tempOrder.symbol = jsonValue['data'][index]['symbol']
                    tempOrder.contract_code = jsonValue['data'][index]['contract_code']
                    tempOrder.contract_type = jsonValue['data'][index]['contract_type']
                    tempOrder.volume = jsonValue['data'][index]['volume']
                    tempOrder.available = jsonValue['data'][index]['available']
                    tempOrder.frozen = jsonValue['data'][index]['frozen']
                    tempOrder.cost_open = jsonValue['data'][index]['cost_open']
                    tempOrder.cost_hold = jsonValue['data'][index]['cost_hold']
                    tempOrder.profit_unreal = jsonValue['data'][index]['profit_unreal']
                    tempOrder.profit_rate = jsonValue['data'][index]['profit_rate']
                    tempOrder.profit = jsonValue['data'][index]['profit']
                    tempOrder.position_margin = jsonValue['data'][index]['position_margin']
                    tempOrder.lever_rate = jsonValue['data'][index]['lever_rate']
                    tempOrder.direction = jsonValue['data'][index]['direction']
                    tempOrder.last_price = jsonValue['data'][index]['last_price']
                    tempOrder.printObj()
                    GDataDMAllOrders.data[tempOrder.direction] = tempOrder


        except Exception as e:
            pprint(e)



    '''
    ======================
    QT注册API
    ======================
    '''
    #测试Excle
    def CallTestOrderXls(self):
        workbook = xlrd.open_workbook('../Resource/order.xls')
        sheet0 = workbook.sheet_by_index(0)

        #总资产
        totalValue = 0.0
        #总手续费
        totalPay = 0.0
        #总盈亏
        totalOrder = 0.0
        #总转入
        totalIn = 0.0

        totalNums = sheet0.nrows
        pprint(totalNums)
        for i in range(totalNums):
            if i < 2 :
                continue
            rowValue = sheet0.row_values(i)
            if rowValue[0] == 'ETH':
                if rowValue[2].find('转入') != -1:
                    totalIn = totalIn + float(rowValue[4])
                continue
            if rowValue[4] == '':
                continue

            #总价
            totalValue = totalValue + float(rowValue[4])

            if rowValue[2].find('手续费') != -1:
                totalPay = totalPay + float(rowValue[4])

            if rowValue[2].find('平多') != -1 or rowValue[2].find('平空') != -1:
                totalOrder = totalOrder + float(rowValue[4])

        totalValue = totalValue + totalIn
        pprint("总资产 ：")
        pprint(totalValue)
        pprint(u"本金")
        pprint(totalIn)
        pprint(u"盈亏")
        pprint(totalOrder)
        pprint(u"手续费")
        pprint(totalPay)
        pass

    #ETH按钮
    def CallBTCInfo(self):
        self.CallSeeBBInfo('BTC')

    #EOS按钮
    def CallEOSInfo(self):
        self.CallSeeBBInfo('EOS')

    #ETH按钮
    def CallETHInfo(self):
        self.CallSeeBBInfo('ETH')

    '''
    ======================
    更新 QT UI
    ======================
    '''
    #账户某个币信息
    def UpdateUIBBInfo(self):
        if not GDataDMBBInfo.status == 'ok' :
            return

        str1 = str(convert2f(GDataDMBBInfo.margin_balance))
        str2 = str(convert2f(GDataDMBBInfo.margin_balance * GDataGlobal.Gindex_price * GUsdt, 0))
        self.__Slate.info1.setText(str1)
        self.__Slate.info21.setText(str2)

        # 已实现盈亏
        str1 = str(convert2f(GDataDMBBInfo.profit_real))
        str2 = str(convert2f(GDataDMBBInfo.profit_real * GDataGlobal.Gindex_price * GUsdt, 0))
        curSheet = "color:green" if GDataDMBBInfo.profit_real >= 0 else "color:red"
        self.__Slate.info2.setStyleSheet(curSheet)
        self.__Slate.info2.setText(str1)
        self.__Slate.info22.setStyleSheet(curSheet)
        self.__Slate.info22.setText(str2)

        #未实现盈亏
        str1 = str(convert2f(GDataDMBBInfo.profit_unreal))
        str2 = str(convert2f(GDataDMBBInfo.profit_unreal * GDataGlobal.Gindex_price * GUsdt, 0))
        curSheet = "color:green" if GDataDMBBInfo.profit_unreal >= 0 else "color:red"
        self.__Slate.info3.setStyleSheet(curSheet)
        self.__Slate.info3.setText(str1)
        self.__Slate.info23.setStyleSheet(curSheet)
        self.__Slate.info23.setText(str2)

        #可用保证金
        str1 = str(convert2f(GDataDMBBInfo.margin_available))
        str2 = str(convert2f(GDataDMBBInfo.margin_available * GDataGlobal.Gindex_price * GUsdt, 0))
        self.__Slate.info4.setText(str1)
        self.__Slate.info24.setText(str2)

        #持仓保证金
        str1 = str(convert2f(GDataDMBBInfo.margin_position))
        str2 = str(convert2f(GDataDMBBInfo.margin_position * GDataGlobal.Gindex_price * GUsdt, 0))
        self.__Slate.info5.setText(str1)
        self.__Slate.info25.setText(str2)

        #冻结资金
        self.__Slate.info6.setText(str(convert2f(GDataDMBBInfo.margin_frozen)))

        #None
        self.__Slate.info7.setText(str(convert2f(GDataDMBBInfo.liquidation_price)))

        self.__Slate.info8.setText(str(convert2f(GDataDMBBInfo.risk_rate)*100) + '%')
        self.__Slate.info9.setText(str(convert2f(GDataDMBBInfo.adjust_factor)))
        self.__Slate.info10.setText(str(convert2f(GDataDMBBInfo.lever_rate)))
        self.__Slate.info11.setText(str(GDataDMBBInfo.symbol))

    #订单信息
    def updateOrdersInfo(self):
        pass


#显示主窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MuMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
