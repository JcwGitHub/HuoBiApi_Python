import sqlite3
import time
from pprint import pprint

#时间
curTime = time.localtime(time.time())
gTableName = str(curTime.tm_year) + str(curTime.tm_mon)

class HuoBiSqlite:
    __sqlite = ''
    __sqliteCur = ''


    def __init__(self):
        pass

    #打开表
    def open(self):
        try:
            self.__sqlite = sqlite3.connect('./../DataBase/HuoBiOrder.db', isolation_level=None)
            """
            PRAGMA wal_autocheckpoint = 1000
            PRAGMA page_size          = 1024
            PRAGMA max_page_count     = 1073741823
            PRAGMA journal_size_limit = -1
            PRAGMA journal_mode       = WAL
            PRAGMA auto_vacuum        = 0
           """
            self.__sqlite.execute('pragma journal_mode=wal;')
            self.__sqlite.execute('PRAGMA wal_autocheckpoint=100;')
            #self.__sqlite.execute('PRAGMA wal_checkpoint;')
            self.__sqliteCur = self.__sqlite.cursor()
            create_tb_cmd = 'CREATE TABLE IF NOT EXISTS [{}](id INTEGER NOT NULL ,ts INTEGER NOT NULL, amount INT,direction TEXT,price DOUBLE);'.format(gTableName)
        except Exception as  e:
            pprint(e)

        # 主要就是上面的语句
        self.__sqliteCur.execute(create_tb_cmd)
        pass

    #提交数据到数据库
    def commit(self):
        self.__sqlite.commit()
        pass

    #关闭数据库
    def close(self):
        self.__sqlite.close()
        pass

    #插入订单数据
    def insertOrder(self,dicValue):
        try:
            #insert_dt_cmd = "INSERT INTO [" + self.__tableName + "](ts,amount,direction,price) VALUES (vdirection,123,vdirection,1.2);"
            #GHuoBiSqlite.insertOrder(var['ts'], var['amount'], var['direction'], var['price'])
            #insert_dt_cmd = 'insert into {1} (ts,id,amount,direction,price) VALUES ({0}{2}{0},{0}{3}{0},{0}{4}{0},{0}{5}{0},{0}{5}{0})'.format("\'",gTableName,str(dicValue['ts']),dicValue['amount'],str(dicValue['direction']),dicValue['price'])
            insert_dt_cmd = 'insert into [{1}] (ts,id,amount,direction,price) VALUES ({ts},{id},{amount},{0}{direction}{0},{price})'.format("\'",gTableName,**dicValue)
            # 主要就是上面的语句
            self.__sqliteCur.execute(insert_dt_cmd)
        except Exception as e:
            print(e.__class__,e)



