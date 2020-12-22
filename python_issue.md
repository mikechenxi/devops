# python issue

## JSON 中文转换

> 转换时增加 ensure_ascii = False 参数

``` python
import json

data = {
    'aa': 'Hello',
    'bb': '你好'
}

return json.dumps(data, ensure_ascii = False)
```

## pymssql 查询结果中文乱码

> 设置编码格式为 cp936

``` python
import pymssql

sql = 'select ....'
conn = pymssql.connect(host='db_host', port=db_port, user='db_user', password='db_password', database='db_name', charset='cp936')
cursor = conn.cursor()
cursor.execute(sql.encode('cp936'))
data = cursor.fetchall()
cursor.close()
conn.close()

return data
```

## django 使用 request.POST.get 无法获取参数

> contentType 为 application/json 时, django 不支持 request.POST.get(), 但可以通过 request.body 来获取 string 类型的参数

``` python
import json

data = request.body
data = json.loads(data)

data.get('xxxx')
```

## datetime.datetime is not JSON serializable

> 使用python自带的json，将数据转换为json数据时，datetime格式的数据报错

> 重写构造json类，遇到日期特殊处理，其余的用内置的就行

``` python
import json
import datetime

class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj)

data = [
    {
        'aa': 'aa',
        'bb': '2020-11-28 10:50:30'
    },
    {
        'cc': 'aa',
        'dd': '2020-11-28 10:51:30'
    }
]

json.dumps(data, cls=DateEncoder)
```
