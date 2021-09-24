import urllib.request
from suds.client import Client
import json


# or just use requests.get, requests.post, requests.put, requests.delete ...
def call_http(url, data = None, method = 'POST', headers = {}, use_proxy = False):
    try:
        if use_proxy:
            proxy_handler = urllib.request.ProxyHandler({'http': 'xxx.xxx.xxx.xxx:80', 'https': 'xxx.xxx.xxx.xxx:80'})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        if data is not None:
            data = bytes(json.dumps(data), 'utf-8')
        headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data, headers)
        req.get_method = lambda: method.upper()
        res = urllib.request.urlopen(req)
        result = res.read()
        return result
    except Exception as e:
        print(e)


# func is one of the functions in this interface
def call_webservice(url, func, data, headers = {}):
    try:
        client = Client(url, headers = headers)
        data_type = type(data).__name__
        expression = 'client.service.' + func + '('
        if data_type == 'tuple' or data_type == 'list':
            for index in range(len(data)):
                if index != 0:
                    expression += ', '
                obj = data[index]
                obj_type = type(obj).__name__
                if obj_type == 'str':
                    expression += '\'' + obj + '\''
                elif obj_type == 'int' or obj_type == 'long' or data_type == 'float' or data_type == 'bool':
                    expression += str(obj)
                else:
                    pass
        elif data_type == 'dict':
            expression += '\'' + json.dumps(data) + '\''
        elif data_type == 'str':
            expression += '\'' + data + '\''
        elif data_type == 'int' or obj_type == 'long' or data_type == 'float' or data_type == 'bool':
            expression += str(data)
        else:
            pass
        expression += ')'
        result = eval(expression)
        return result
    except Exception as e:
        print(e)



# get session
# use 'print client_login' will get all functions of this webservice interface
# use 'print result' will get all properties and functions of this instance
# login() is one of the functions in this interface
'''
result:
(WSContext){
   dbType = 'dbType'
   dcName = "dcName"
   password = "password"
   sessionId = "e2b4eaf7-f424-4544-93a1-sssssssssss"
   slnName = slnNameeas"
   userName = "userName"
 }
''' 
login_url = 'http://ip:port/ormrpc/services/EASLogin?wsdl'
login_client = Client(url)
result = login_client.service.login('userName', 'password', 'slnName', 'dcName', 'language', 'dbType')
session_id = result.sessionId

# get bank
'''
result:
{
    "totalSize":1053,
    "data":[
        {
            "number":"123456789",
            "province":"北京市",
            "city":"北京市",
            "name":"中国人民银行XXX支行"
        },
        {
            "number":"987654321",
            "province":"天津市",
            "city":"天津市",
            "name":"中国人民银行XX分行XXX支行"
        }
    ],
    "success":true
}
'''
headers = {'SessionId':session_id}
query_bank_url = 'http://ip:port/ormrpc/services/WSFcInterfaceFacade?wsdl'
query_bank_client = Client(query_bank_url, headers = headers)
dic = {
    "offset": 0,
    "limit": 2
}
result = query_bank_client.service.queryBEBank(json.dumps(dic))
result = json.loads(result)
if result['success'] == True:
    return result['data']
