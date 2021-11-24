# python issue

## windows 上 python2 和 python3 共存

```
python3 安装目录中修改 python.exe 为 python3.exe, pythonw.exe 为 pythonw3.exe
python3 -m pip install --upgrade pip --force-reinstall  # python3
python -m pip install --upgrade pip --force-reinstall  # python2
```

https://www.cnblogs.com/qzf-kuku/p/10248891.html

## centos6 中 python3 ImportError: No module named _ssl

 - openssl版本太低, 需要升级 openssl

```
cd /home/openssl-1.1.0l
./config --prefix=/usr/local/openssl-1.1.01
make
make install

vim /etc/ld.so.conf.d/openssl.conf
录入 /usr/local/openssl-1.1.01/lib/ 保存
更新共享库
ldconfig
检验 openssl-1.1.1 是否已加入共享库
ldconfig -v | grep ssl

/usr/local/openssl-1.1.01/lib:
    libssl.so.1.1 -> libssl.so.1.1    '''有这个表示加成功了'''
    libssl3.so -> libssl3.so
    libssl.so.10 -> libssl.so.1.0.1e

cd /home/Python-3.7.5/
./configure --prefix=/usr/local/python3.7 --with-openssl=/usr/local/openssl-1.1.01
make && make install

ln -s /usr/local/python3.7/bin/python3.7 /usr/bin/python3.7
ln -s /usr/bin/python3.7 /usr/bin/python3
ln -s /usr/local/python3.7/bin/pip3.7 /usr/bin/pip3.7
ln -s /usr/bin/pip3.7 /usr/bin/pip3
```

https://blog.51cto.com/tchuairen/2435472

## centos6 安装新版本 openssl 后安装 uwsgi 出现关于SSL错误的问题 

 - openssl 版本比较久 或者系统存在多个openssl 版本 移除旧版本openssl

```
yum remove openssl-devel
```

https://www.cnblogs.com/shmily3929/p/10109182.html

https://blog.csdn.net/rongdang/article/details/102871874

## uwsgi + flask_apscheduler 定时任务不执行

 - 原因：uwsgi 默认one thread one processor ,所以在没有请求的时候，导致部分进程被挂起
 - 解决方法：在uwsgi配置中添加enable-threads = true

## python3 提示 certificate verify failed: unable to get local issuer certificate

  - 错误原因：这是一个SSL证书验证错误，当请求一个https站点，但是证书验证错误时，就会报这样的错误。
  - 解决方法：只需在代码中加入如下两行将跳过证书的检查，即可成功访问网页。

``` python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

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
param= ('', '')
conn = pymssql.connect(host='db_host', port=db_port, user='db_user', password='db_password', database='db_name', charset='cp936')
cursor = conn.cursor()
cursor.execute(sql.encode('cp936'), param.encode('cp936'))
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
import json, datetime

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

## 'Decimal' is not JSON serializable

``` python
import json, decimal

class DecimalEncoder(json.JSONEncoder):
　　def default(self, o):
　　　　if isinstance(o, decimal.Decimal):
　　　　　　return float(o)
　　　　super(DecimalEncoder, self).default(o)

json.dumps(ret_list, cls=DecimalEncoder)
```

## list 和 dictionary 排序

``` python
#list
li = [('2021-02-21', 'aa'), ('2021-01-02', 'cc'), ('2021-03-03', 'bb')]
li.sort()
print(li) # [('2021-01-02', 'cc'), ('2021-02-21', 'aa'), ('2021-03-03', 'bb')]
li.sort(reverse = True)  
print(li) # [('2021-03-03', 'bb'), ('2021-02-21', 'aa'), ('2021-01-02', 'cc')]
li.sort(key = lambda x:x[1])
print(li) # [('2021-02-21', 'aa'), ('2021-03-03', 'bb'), ('2021-01-02', 'cc')]


# dic
dic = {
	'2021-02-21' :'aa',
	'2021-01-02': 'cc',
	'2021-03-03': 'bb'
}
dic2 = {}
for key in sorted(dic.keys()):
    dic2[key] = dic[key]
print(dic2) # {'2021-01-02': 'cc', '2021-02-21': 'aa', '2021-03-03': 'bb'}
dic2 = {}
for key in sorted(dic.keys(), reverse = True):
    dic2[key] = dic[key]
print(dic2) # {'2021-03-03': 'bb', '2021-02-21': 'aaa', '2021-01-02': 'cc'}
print(sorted(dic.items(), key=lambda item:item[1]))  # [('2021-02-21', 'aa'), ('2021-03-03', 'bb'), ('2021-01-02', 'cc')] 按value排序后转乘list
```

## python datetimie

``` python
[in]import datetime

[in]: datetime.datetime.now()
[out]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696)
[in]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696).timestamp()
[out]: 1616638918.557696
[in]: datetime.datetime.fromtimestamp(1616638918.557696)
[out]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696)

[in]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696).strftime('%Y-%m-%d %H:%M:%S')
[out]: '2021-03-25 10:21:58'
[in]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696).strftime('%Y-%m-%d')
[out]: '2021-03-25'
[in]: datetime.datetime(2021, 3, 25, 10, 21, 58, 557696).strftime('%H:%M:%S')
[out]: '10:21:58'

[in]: datetime.datetime.strptime('2021-03-25 10:23:22', '%Y-%m-%d %H:%M:%S')
[out]: datetime.datetime(2021, 3, 25, 10, 23, 22)
[in]: datetime.datetime.strptime('2021-03-25', '%Y-%m-%d')
[out]: datetime.datetime(2021, 3, 25, 0, 0)
[in]: datetime.datetime.strptime('10:23:22', '%H:%M:%S')
[out]: datetime.datetime(1900, 1, 1, 10, 23, 22)

[in]: datetime.datetime(2021, 4, 28, 15, 34, 56, 52) - datetime.datetime(2020, 3, 25, 10, 23, 22)
[out]: datetime.timedelta(days=399, seconds=18694, microseconds=52)
[in]: datetime.datetime(2001, 3, 25, 10, 23, 22) + datetime.timedelta(days = 1, hours = 1, minutes = 1, seconds = 1, microseconds = 1)
[out]: datetime.datetime(2001, 3, 26, 11, 24, 23, 1)
```

## ModuleNotFoundError: No module named '_bz2'

缺少_bz2.cpython-36m-x86_64-linux-gnu.so文件，将_bz2.cpython-36m-x86_64-linux-gnu.so文件放入python安装目录/usr/local/python3.7/lib/python3.7/lib-dynload

https://github.com/mikechenxi/devops/blob/main/python/_bz2.cpython-37m-x86_64-linux-gnu.so
