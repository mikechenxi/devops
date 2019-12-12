#!/usr/bin/python
# -*- coding: utf-8 -*

from suds.client import Client
import json

# get session
# use 'print client_login' will get all functions of this webservice interface
# login() is one of the functions in this interface
login_url = 'http://ip:port/ormrpc/services/EASLogin?wsdl'
login_client = Client(url)
result = login_client.service.login('userName', 'password', 'slnName', 'dcName', 'language', dbType)
session_id = result[3]

# get bank data
headers = headers={'SessionId':session_id}
wsfc_interface_facade_url = 'http://ip:port/ormrpc/services/WSFcInterfaceFacade?wsdl'
wsfc_interface_facade_client = Client(wsfc_interface_facade_url, headers = headers)
dic = {
    "offset": 0,
    "limit": 10
}
result = wsfc_interface_facade_client.service.queryBEBank(json.dumps(dic))
result = json.loads(result)
if result['success'] == True:
    return result['data']
