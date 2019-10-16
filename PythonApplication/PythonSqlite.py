import sqlite3
from pprint import pprint






'''''
PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM [201910];

DROP TABLE [201910];

CREATE TABLE [201910] (
    ts        STRING NOT NULL,
    amount    INT,
    direction STRING,
    price     DOUBLE
);

INSERT INTO [201910] (
                         ts,
                         amount,
                         direction,
                         price
                     )
                     SELECT ts,
                            amount,
                            direction,
                            price
                       FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;
'''''


class HuoBiSqlite:
    __sqlite = ''
    __sqliteCur = ''
    __tableName = '[201910]'

    def __init__(self):
        pass

    #打开表
    def open(self):
        self.__sqlite = sqlite3.connect('HuoBiOrder.db')
        self.__sqliteCur = self.__sqlite.cursor()
        create_tb_cmd = "CREATE TABLE IF NOT EXISTS " + self.__tableName + "(ts STRING NOT NULL, amount INT,direction STRING,price DOUBLE);"

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
            insert_dt_cmd = 'insert into {0} (ts,amount,direction,price) VALUES ({1:s},{2},{3:s},{4})'.format(self.__tableName,str(dicValue['ts']),dicValue['amount'],str(dicValue['direction']),dicValue['price'])
            # 主要就是上面的语句
            self.__sqliteCur.execute(insert_dt_cmd)
        except Exception as e:
            print('错误类型是', e.__class__.__name__)
            print('错误明细是', e)
            pprint('insertOrder error')
        pass



