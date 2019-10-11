import sys
import json
import threading
import time

import xlrd
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

import PythonApplicationUI
from HuobiDMService import HuobiDM
from pprint import pprint


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
        self.__Slate.pushButton.clicked.connect(self.CallBtn1)
        pass

    #测试
    def CallBtn1(self):
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

#显示主窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = PythonApplicationUI.Ui_MainWindow()
    MainWindow = MuMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.SetUI(ui)
    MainWindow.show()
    sys.exit(app.exec_())
