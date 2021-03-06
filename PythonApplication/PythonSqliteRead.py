﻿import sqlite3
import time
from pprint import pprint


#时间
curTime = time.localtime(time.time())
gTableName ='[' + str(curTime.tm_year) + str(curTime.tm_mon) + ']'


class HuoBiSqliteRead:
    __sqlite = ''
    __sqliteCur = ''
    __tableCur = ''
    __nums = 0


    def __init__(self):
        pass

    #打开表
    def open(self):
        try:
            self.__sqlite = sqlite3.connect('./DataBase/HuoBiOrder.db', isolation_level=None)
            self.__sqlite.execute('pragma journal_mode=wal;')

            #self.__sqliteCur = self.__sqlite.execute('SELECT * from {}'.format(gTableName))
            self.__sqliteCur = self.__sqlite.cursor()
        except Exception as  e:
            pprint(e)

    def getOrderLastLines(self,lines):
        # 表头
        # self.__tableCur = self.__sqliteCur.execute('SELECT * FROM {}'.format(gTableName))
        cur1 = time.time()
        self.__tableCur = self.__sqliteCur.execute('SELECT * FROM {} ORDER BY id DESC limit {}'.format(gTableName,lines))
        cur2 = time.time()
        pprint(cur2 - cur1)
        return self.__tableCur.fetchall()



#测试
if __name__ == '__main__':
    sqlRead = HuoBiSqliteRead()
    sqlRead.open()

    while 1:
        time.sleep(2)
        #pprint(sqlRead.getAllLineNums())
    pass