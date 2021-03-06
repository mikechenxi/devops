#!/usr/bin/python
# -*- coding: utf-8 -*-
# MySQL & SQL Server

import pymysql, pymssql, collections, sys
reload(sys)
sys.setdefaultencoding('utf-8')


def query_mysql(sql, param = None):
    db_server = 'xxx.xxx.xxx.xxx'
    db_port = 3306
    db_user_name = 'user_name'
    db_password = 'password'
    db_name = 'db_name'

    try:
        conn = pymysql.connect(host = db_server, port = db_port, user = db_user_name, passwd = db_password, db = db_name)
        cursor = conn.cursor()
        cursor.execute(sql, param)
        result = cursor.fetchall()
        fields = cursor.description
        cursor.close()
        conn.close()
        res = format_data(result, fields)
        return res
    except Exception as e:
        print(e)


def execute_mysql(sql, param = None):
    db_server = 'xxx.xxx.xxx.xxx'
    db_port = 3306
    db_user_name = 'user_name'
    db_password = 'password'
    db_name = 'db_name'

    try:
        conn = pymysql.connect(host = db_server, port = db_port, user = db_user_name, passwd = db_password, db = db_name)
        cursor = conn.cursor()
        count = cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(e)


def query_mssql(sql, param = None):
    db_server = 'xxx.xxx.xxx.xxx'
    db_port = 1433
    db_user_name = 'user_name'
    db_password = 'password'
    db_name = 'db_name'

    try:
        conn = pymssql.connect(host = db_server, port = db_port, user = db_user_name, password = db_password, database = db_name)
        cursor = conn.cursor()
        cursor.execute(sql, param)
        result = cursor.fetchall()
        fields = cursor.description
        cursor.close()
        conn.close()
        res = format_data(result, fields)
        return res
    except Exception as e:
        print(e)


def execute_mssql(sql, param = None):
    db_server = 'xxx.xxx.xxx.xxx'
    db_port = 1433
    db_user_name = 'user_name'
    db_password = 'password'
    db_name = 'db_name'

    try:
        conn = pymssql.connect(host = db_server, port = db_port, user = db_user_name, password = db_password, database = db_name)
        cursor = conn.cursor()
        count = cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(e)

# result: ((), ()), fields: ((), ())
def format_data(result, fields):
    # ???????????? ['id', 'name', 'password']
    field = []
    for i in fields:
        field.append(i[0])
    # ????????????????????? ??????[{'id': 1, 'name': 'admin', 'password': '123456'}]
    res = []
    for iter in result:
        line_data = collections.OrderedDict()
        for index in range(0, len(field)):
            line_data[field[index]] = iter[index]
        res.append(line_data)
    return res
