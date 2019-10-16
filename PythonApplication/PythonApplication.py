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
from HuobiData import GDataDMInfo, GDataGlobal, GDataDMBBInfo, Datacontract_index
from PythonSqlite import GHuoBiSqlite

#QT
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction
#QT UI
import PythonApplicationUI

#huoBi API
from HuobiDMService import HuobiDM
from huobi import GHuoBiDingYue

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
    #QT UI
    __Slate = ''
    #火币API
    __HBAPI = ''
    #线程
    __ThreadName__ = ''
    __ThreadFinish = 0
    __threadHY = ''
    __threadHYFinish = 0

    def __init__(self):
        QMainWindow.__init__(self)

        URL = ''
        ACCESS_KEY = ''
        SECRET_KEY = ''

        #读取key
        with open('C:\HuoBiKey.json', 'r') as loadf:
            load_dict = json.load(loadf)
            URL = load_dict['URL']
            ACCESS_KEY = load_dict['Access_Key']
            SECRET_KEY = load_dict['Secret_Key']

        # 初始化账号
        self.__HBAPI = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)

        #开启多线程
        __ThreadName__ = threading.Thread(target=self.ThreadUpdate)
        __ThreadName__.start()
        __threadHY = threading.Thread(target=self.threadHY)
        __threadHY.start()
        pass

    #合约订阅线程
    def threadHY(self):
        GHuoBiDingYue.Connect()
        while self.__threadHYFinish == 0:
            GHuoBiDingYue.tick()


    #定时更新线程
    def ThreadUpdate(self):
        GDataGlobal.GThreadFrames = 0
        delayTime = 1

        while self.__ThreadFinish == 0:
            if GDataGlobal.GCurSymbol:
                #初始化,币基础信息
                if GDataGlobal.GThreadFrames == 0:
                    self.CallContract_info()

                #更新指数信息
                if GDataGlobal.GThreadFrames % 5 == 0:
                    self.Callcontract_index()

                # 更新当前账户信息
                if GDataGlobal.GThreadFrames % 5 == 0:
                    self.Callcontract_account_info()
                    self.UpdateUIBBInfo()

                GDataGlobal.GThreadFrames += delayTime
                #GDataGlobal.GCurSymbol if end

            time.sleep(delayTime)

    #初始化UI
    def SetUI(self , slate):
        self.__Slate = slate
        self.__Slate.BTNEOS.clicked.connect(self.CallEOSInfo)
        self.__Slate.BTNETH.clicked.connect(self.CallETHInfo)
        pass



    '''
    ======================
    函数API
    ======================
    '''
    #查看某个币种
    def CallSeeBBInfo(self,symbol):
        GDataGlobal.GCurSymbol =symbol
        GDataGlobal.GThreadFrames = 0
        pass

    #获取合约信息
    def CallContract_info(self):
        if not GDataGlobal.GCurSymbol:
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
        except:
            pprint('CallContract_info Error')
            pass



    #获取账户信息
    def Callcontract_account_info(self):
        if not GDataGlobal.GCurSymbol:
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
        except:
            pprint('Callcontract_account_info Error')
            pass

    #获取合约指数信息
    def Callcontract_index(self):
        if not GDataGlobal.GCurSymbol:
            return
        try:
            jsonValue = self.__HBAPI.get_contract_index(GDataGlobal.GCurSymbol)
            if jsonValue['status'] == 'ok':
                GDataGlobal.Gindex_price = convert2f(jsonValue['data'][0]['index_price'])
            # GDataGlobal.printObj()
        except:
            pass

    '''
    ======================
    QT注册
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

    #EOS按钮/程序退出
    def CallEOSInfo(self):
        #停止线程
        self.__ThreadFinish = 1
        self.__threadHYFinish = 1
        #关闭数据库
        GHuoBiSqlite.close()
        #退出程序
        sys.exit(0)
        pass

    #ETH按钮
    def CallETHInfo(self):
        self.CallSeeBBInfo('ETH')
        pass

    '''
    ======================
    更新 QT UI
    ======================
    '''
    #账户某个币信息
    def UpdateUIBBInfo(self):
        if not GDataDMBBInfo.status == 'ok' :
            return

        #输出当前属性
        GDataDMBBInfo.printObj()

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
        pass



#显示主窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = PythonApplicationUI.Ui_MainWindow()
    MainWindow = MuMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.SetUI(ui)
    MainWindow.show()
    sys.exit(app.exec_())

    pass
