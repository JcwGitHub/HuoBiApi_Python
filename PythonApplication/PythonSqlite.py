import sqlite3
from pprint import pprint


GSqlite = sqlite3.connect('HuoBiOrder.db')
GSqliteCur = GSqlite.cursor()

class HuoBiSqlite:
    def __init__(self):
        pass

    #打开表
    def openTable(self):
        create_tb_cmd = "CREATE TABLE IF NOT EXISTS USER(NAME TEXT, AGE INT,SALARY REAL)"
        pass

    #关闭表
    def closeTable(self):
        pass

    #关闭数据库
    def close(self):
        GSqlite.commit()
        GSqlite.close()
        pass

GHuoBiSqlite = HuoBiSqlite()




