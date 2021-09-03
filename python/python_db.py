#!/usr/bin/python
# -*- coding: utf-8 -*-
# MySQL & SQL Server

import pymysql, pymssql, collections, sys
reload(sys)
sys.setdefaultencoding('utf-8')


def query_mysql(sql, param = None, return_column_names = True):
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
        if return_column_names == True:
            res = format_data(result, fields)
            return res
        else:
            return result
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
        cursor.execute(sql, param)
        count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(e)


def query_mssql(sql, param = None, return_column_names = True):
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
        if return_column_names == True:
            res = format_data(result, fields)
            return res
        else:
            return result
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
        cursor.execute(sql, param)
        count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(e)


# result: ((), ()), fields: ((), ())
def format_data(result, fields):
    # 字段数组 ['id', 'name', 'password']
    field = []
    for i in fields:
        field.append(i[0])
    # 返回的数组集合 形式[{'id': 1, 'name': 'admin', 'password': '123456'}]
    res = []
    for iter in result:
        line_data = collections.OrderedDict()
        for index in range(0, len(field)):
            line_data[field[index]] = iter[index]
        res.append(line_data)
    return res
