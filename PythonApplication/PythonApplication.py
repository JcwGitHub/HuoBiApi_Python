
import json

from HuobiDMService import HuobiDM
from pprint import pprint

#### input huobi dm url
URL = ''
ACCESS_KEY = ''
SECRET_KEY = ''

####  input your access_key and secret_key below:
with open('C:\HuoBiKey.json','r') as loadf :
    load_dict = json.load(loadf)
    URL = load_dict['URL']
    ACCESS_KEY = load_dict['Access_Key']
    SECRET_KEY = load_dict['Secret_Key']
    pprint(URL)
    pprint(ACCESS_KEY)
    pprint(SECRET_KEY)

#初始化账号
dm = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)

print (u' 获取用户账户信息 ')
pprint (dm.get_contract_account_info())
pprint (dm.get_contract_account_info("EOS"))