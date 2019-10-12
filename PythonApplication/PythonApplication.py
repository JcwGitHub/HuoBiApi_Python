import sys
import json
import threading
import time

import xlrd
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

import PythonApplicationUI
from HuobiDMService import HuobiDM
from pprint import pprint

#数据结构
from HuobiData import GDataDMInfo, GDataGlobal, GDataDMBBInfo


class MuMainWindow(QMainWindow):
    __Slate = ''
    __HBAPI = ''
    __SearchName = 'EOS_CW'

    def __init__(self):
        QMainWindow.__init__(self)

        #### input huobi dm url
        URL = ''
        ACCESS_KEY = ''
        SECRET_KEY = ''

        ####  input your access_key and secret_key below:
        with open('C:\HuoBiKey.json', 'r') as loadf:
            load_dict = json.load(loadf)
            URL = load_dict['URL']
            ACCESS_KEY = load_dict['Access_Key1']
            SECRET_KEY = load_dict['Secret_Key1']
            pprint(URL)
            pprint(ACCESS_KEY)
            pprint(SECRET_KEY)

        # 初始化账号
        self.__HBAPI = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)

        #创建查询线程
        # try:
        #   newThread = threading.Thread(target=self.ThreadUpdateDepth)
        #   newThread.start()
        #except:
        #    pprint("Error: unable to start thread")

        pass

    #定时更新线程
    def ThreadUpdateDepth(self):
        while 1 :
            if self.__SearchName != '' :
                jsonValue = self.__HBAPI.get_contract_depth('EOS_CW', 'step1')
                pprint(jsonValue)
            pass
        time.sleep(1)
        pass

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
    #获取合约信息
    def CallContract_info(self):
        if not GDataGlobal.GCurSymbol:
            return

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
        GDataDMInfo.printObj()
        pass

    #获取账户信息
    def Callcontract_account_info(self):
        if not GDataGlobal.GCurSymbol:
            return
        jsonValue = self.__HBAPI.get_contract_account_info(GDataGlobal.GCurSymbol)
        GDataDMBBInfo.status = jsonValue['status']
        GDataDMBBInfo.symbol = jsonValue['data'][0]['symbol']
        GDataDMBBInfo.margin_balance = jsonValue['data'][0]['margin_balance']
        GDataDMBBInfo.margin_position = jsonValue['data'][0]['margin_position']
        GDataDMBBInfo.margin_frozen	 = jsonValue['data'][0]['margin_frozen']
        GDataDMBBInfo.margin_available = jsonValue['data'][0]['margin_available']
        GDataDMBBInfo.profit_real = jsonValue['data'][0]['profit_real']
        GDataDMBBInfo.profit_unreal = jsonValue['data'][0]['profit_unreal']
        GDataDMBBInfo.risk_rate = jsonValue['data'][0]['risk_rate']
        GDataDMBBInfo.liquidation_price = jsonValue['data'][0]['liquidation_price']
        GDataDMBBInfo.withdraw_available = jsonValue['data'][0]['withdraw_available']
        GDataDMBBInfo.lever_rate = jsonValue['data'][0]['lever_rate']
        GDataDMBBInfo.adjust_factor = jsonValue['data'][0]['adjust_factor']
        GDataDMBBInfo.printObj()
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

    #EOS按钮
    def CallEOSInfo(self):
        GDataGlobal.GCurSymbol = 'EOS'
        self.CallContract_info()
        self.Callcontract_account_info()
        self.UpdateUIBBInfo()
        pass

    #ETH按钮
    def CallETHInfo(self):
        GDataGlobal.GCurSymbol = 'ETH'
        self.CallContract_info()
        self.Callcontract_account_info()
        self.UpdateUIBBInfo()
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

        self.__Slate.info1.setText(str(GDataDMBBInfo.margin_balance))

        if GDataDMBBInfo.profit_real >= 0:
            self.__Slate.info2.setStyleSheet("color:green")
        else:
            self.__Slate.info2.setStyleSheet("color:red")
        self.__Slate.info2.setText(str(GDataDMBBInfo.profit_real))

        if GDataDMBBInfo.profit_unreal >= 0:
            self.__Slate.info3.setStyleSheet("color:green")
        else:
            self.__Slate.info3.setStyleSheet("color:red")
        self.__Slate.info3.setText(str(GDataDMBBInfo.profit_unreal))
        self.__Slate.info4.setText(str(GDataDMBBInfo.margin_available))
        self.__Slate.info5.setText(str(GDataDMBBInfo.margin_position))
        self.__Slate.info6.setText(str(GDataDMBBInfo.margin_frozen))
        self.__Slate.info7.setText(str(GDataDMBBInfo.liquidation_price))
        self.__Slate.info8.setText(str(GDataDMBBInfo.risk_rate))
        self.__Slate.info9.setText(str(GDataDMBBInfo.adjust_factor))
        self.__Slate.info10.setText(str(GDataDMBBInfo.lever_rate))
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
