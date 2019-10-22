from pprint import pprint



""""""
#Root
""""""
class DataRoot(object):
    status = 'error'
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
    #线程更新总次数
    GThreadFrames = 0
    #USDT价格
    GUSDT = 7.1

GDataGlobal = DataGlobal()


""""""
#合约信息
""""""
class DataDMInfo(DataRoot) :
    #品种代码
    symbol = ''
    #合约代码
    contract_code = ''
    #合约类型
    contract_type = ''
    #合约面值，即1张合约对应多少美元
    contract_size = ''
    #合约价格最小变动精度
    price_tick = ''
    #合约交割日期
    delivery_date = ''
    #合约上市日期
    create_date = ''
    #合约状态
    contract_status = ''

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

GDataDMBBInfo = DataDMBBInfo()


#用户某个币持仓信息
class DataDMAllOrder(DataRoot):
    symbol = ''
    # 合约代码 "BTC180914" ...
    contract_code = ''
    # 合约类型 当周:"this_week", 次周:"next_week", 季度:"quarter"
    contract_type = ''
    #持仓量
    volume = 0
    #可平仓数量
    available = 0
    #冻结数量
    frozen = 0
    #开仓均价
    cost_open = 0.0
    #持仓均价
    cost_hold = 0.0
    #未实现盈亏
    profit_unreal = 0.0
    #收益率
    profit_rate = 0.0
    #收益
    profit = 0.0
    #持仓保证金
    position_margin = 0.0
    #杠杠倍数
    lever_rate = 0
    #"buy":买 "sell":卖
    direction = ''
    #最新价
    last_price = 0.0

class DataDMAllOrders(DataRoot):
    data = list()
GDataDMAllOrders = DataDMAllOrders()

#指数信息
class Datacontract_index(DataRoot):
    symbol = ''
    index_price =''
    index_ts = ''
    ts =''


#下单数据
class DataOrderInfo(DataRoot):
    symbol = ''
    contract_type = 'this_week'
    #USDT
    price = 0.0
    #张
    volume = 0
    #"buy":买 "sell":卖
    direction = ''
    #"open":开仓 "close":平仓
    offset = ''
    #杠杆
    lever_rate = 0
    #订单报价类型 "limit":限价 "opponent":对手价 "post_only":只做maker单,post only下单只受用户持仓数量限制,
    # optimal_5：最优5档、optimal_10：最优10档、optimal_20：最优20档，ioc:IOC订单，fok：FOK订单
    #对手价下单price价格参数不用传，对手价下单价格是买一和卖一价, optimal_5：最优5档、optimal_10：最优10档、optimal_20：最优20档下单price价格参数不用传，"limit": 限价，"post_only": 只做maker单
    #需要传价格，"fok"：全部成交或立即取消，"ioc": 立即成交并取消剩余。
    order_price_type = ''

GDataOrderInfo = DataOrderInfo()