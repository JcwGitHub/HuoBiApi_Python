from pprint import pprint



""""""
#Root
""""""
class DataRoot(object):
    status = ''
    impDataUpdate = ''
    #打印信息
    def printObj(self):
        pprint(self.__dict__)
        pass
    pass

    #是否有效
    def isValid(self):
        return self.status == 'ok'

    #数据更新回调函数

#全局信息
class DataGlobal(DataRoot):
    # 当前币种
    GCurSymbol = ''
    # 当前指数信息，当前价位
    Gindex_price = ''
    pass
GDataGlobal = DataGlobal()


""""""
#合约信息
""""""
class DataDMInfo(DataRoot) :
    symbol = ''
    contract_code = ''
    contract_type = ''
    contract_size = ''
    price_tick = ''
    delivery_date = ''
    create_date = ''
    contract_status = ''
    pass
GDataDMInfo = DataDMInfo()


""""""
#合约某个币信息
""""""
class DataDMBBInfo(DataRoot):
    #data
    #币种类
    symbol = ''
    #账户权益
    margin_balance = ''
    #持仓保证金（当前持有仓位所占用的保证金）
    margin_position = ''
    #冻结保证金
    margin_frozen = ''
    #可用保证金
    margin_available = ''
    #已实现盈亏
    profit_real = ''
    #未实现盈亏
    profit_unreal = ''
    #保证金率
    risk_rate = ''
    #预估强平价
    liquidation_price = ''
    #可划转数量
    withdraw_available = ''
    #杠杠倍数
    lever_rate = ''
    #调整系数
    adjust_factor = ''
    #list
    ts = ''
    pass
GDataDMBBInfo = DataDMBBInfo()

class Datacontract_index(DataRoot):
    symbol = ''
    index_price =''
    index_ts = ''
    ts =''
    pass