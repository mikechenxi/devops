#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from suds.client import Client
import json

def call_http(url, data, method = '', headers = {}):
    try:
        method = method.upper()
        req = urllib2.Request(url, data)
        if len(headers) > 0:
            for header in headers:
                req.add_header(header, headers[header])
        req.add_header('Content-Type', 'application/json')
        if method == 'PUT' or method == 'DELETE':
            req.get_method = lambda: method
        res = urllib2.urlopen(req)
        #opener = urllib2.build_opener()
        #res = opener.open(url, data)
        return res.read()
    except Exception as e:
        print e


# func is one of the functions in this interface
def call_webservice(url, func, data, headers = {}):
    try:
        client = None
        if len(headers) > 0:
            client = Client(url, headers = headers)
        else:
            client = Client(url)
        data_type = type(data).__name__
        expression = 'client.service.' + func + '('
        if data_type == 'tuple' or data_type == 'list':
            for index in range(len(data)):
                if index != 0:
                    expression += ', '
                obj = data[index]
                obj_type = type(obj).__name__
                if obj_type == 'int' or data_type == 'float' or data_type == 'bool':
                    expression += str(data[index])
                elif obj_type == 'str':
                    expression += '\'' + obj + '\''
                else:
                    pass
        elif data_type == 'dict':
            expression += '\'' + json.dumps(data) + '\''
        elif data_type == 'str':
            expression += '\'' + data + '\''
        elif data_type == 'int' or data_type == 'float' or data_type == 'bool':
            expression += str(data)
        else:
            pass
        expression += ')'
        result = eval(expression)
        return result
    except Exception as e:
        print e



# get session
# use 'print client_login' will get all functions of this webservice interface
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
session_id = result[3]

# get bank data
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
wsfc_interface_facade_url = 'http://ip:port/ormrpc/services/WSFcInterfaceFacade?wsdl'
wsfc_interface_facade_client = Client(wsfc_interface_facade_url, headers = headers)
dic = {
    "offset": 0,
    "limit": 2
}
result = wsfc_interface_facade_client.service.queryBEBank(json.dumps(dic))
result = json.loads(result)
if result['success'] == True:
    return result['data']


