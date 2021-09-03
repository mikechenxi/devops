# apache 使用 mod_jk 模块配置 AJP协议 反向代理

> 工作目录目录为 /home

## 1.安装依赖包 

```
yum install  gcc gcc-c++
```

## 2.下载软件 apr、apr-util、pcre、httpd、mod_jk

```
wget http://mirrors.tuna.tsinghua.edu.cn/apache/apr/apr-1.7.0.tar.gz
wget http://mirrors.tuna.tsinghua.edu.cn/apache/apr/apr-util-1.6.1.tar.gz
wget ftp://ftp.pcre.org/pub/pcre/pcre-8.43.tar.gz
wget http://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.43.tar.gz
wget http://mirror.bit.edu.cn/apache/tomcat/tomcat-connectors/jk/tomcat-connectors-1.2.48-src.tar.gz
```

## 3.安装 apr

```
tar -xzvf apr-1.7.0.tar.gz
cd apr-1.7.0
./configure --prefix=/app/apr-1.7.0
make
make install
```

## 4.安装 apr-util

```
tar -xzvf apr-util-1.6.1.tar.gz
cd apr-util-1.6.1
./configure --prefix=/app/apr-util-1.6.1 --with-apr=/app/apr-1.7.0/bin/apr-1-config
make
make install
```

如果安装 apr-util 提示 expat.h: No such file or directory, 需要安装 expat-devel

在线安装 expat-devel

```
yum install expat-devel
```

离线安装 expat-devel

```
wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/expat/2.0.1-7.2/expat_2.0.1.orig.tar.gz
tar -xzvf expat_2.0.1.orig.tar.gz
cd expat_2.0.1
./configure
make
make install
```

## 5.安装 pcre

```
tar -xzvf pcre-8.43.tar.gz
cd pcre-8.43
./configure --prefix=/app/pcre-8.43 --with-apr=/app/apr-1.7.0/bin/apr-1-config
make
make install
```

## 6.安装 apache

```
tar -xzvf httpd-2.4.43.tar.gz
cd httpd-2.4.43
./configure --prefix=/app/httpd-2.4.43 --enable-deflate=shared --with-pcre=/app/pcre-8.43 --with-apr=/app/apr-1.7.0 --with-apr-util=/app/apr-util-1.6.1
make
make install
```

## 7.安装 mod_jk

```
tar -xzvf tomcat-connectors-1.2.48-src.tar.gz
cd tomcat-connectors-1.2.48-src/native/
./configure --with-apxs=/app/httpd-2.4.43/bin/apxs
make
make install
```

## 8.配置 apache

编辑 /app/httpd-2.4.43/conf/httpd.conf, 末尾加上 

```
LoadModule deflate_module modules/mod_deflate.so

Include conf/mod_jk.conf
AddOutputFilterByType DEFLATE text/html text/plain text/xml
```

/app/httpd-2.4.43/conf/ 目录新建 mod_jk.conf, 内容如下

```
LoadModule jk_module modules/mod_jk.so

JkWorkersFile conf/workers.properties
JkMountFile conf/uriworkermap.properties
JkLogFile logs/mod_jk.log
JkLogLevel info
#format
JkLogStampFormat "[%a %b %d %H:%M:%S %Y]"
#options
JkOptions +ForwardKeySize +ForwardURICompat -ForwardDirectories
JkRequestLogFormat "%w %V %T %B %H %m %r %s %U %v %q %p %R"
#JkRequestLogFormat "%w %V %T"
JkMount /* controller
HostnameLookups Off

# Should mod_jk send SSL information to Tomcat (default is On)
JkExtractSSL On
# What is the indicator for SSL (default is HTTPS)
JkHTTPSIndicator HTTPS
# What is the indicator for SSL session (default is SSL_SESSION_ID)
JkSESSIONIndicator SSL_SESSION_ID
# What is the indicator for client SSL cipher suit (default is SSL_CIPHER)
JkCIPHERIndicator SSL_CIPHER
# What is the indicator for the client SSL certificated (default is SSL_CLIENT_CERT)
JkCERTSIndicator SSL_CLIENT_CERT
```

/app/httpd-2.4.43/conf/ 目录新建 workers.properties, 内容如下

```
worker.list = controller,status 
worker.status.type=status
worker.controller.type=lb

worker.controller.balance_workers=app

worker.controller.sticky_session=1
worker.controller.sticky_session_force=0

worker.app.port=8009
worker.app.host=192.168.189.133
worker.app.type=ajp13
worker.app.lbfactor=1
worker.app.retries=3

# 192.168.189.133为tomcat所在服务器, 8009为tomcat ajp协议端口
```

/app/httpd-2.4.43/conf/ 目录新建 uriworkermap.properties, 内容如下

```
/*=controller
/jkstatus= status
```

## 9.启动、停止、重启、不中断当前连接重启 apache

```
cd /app/httpd-2.4.43/bin
./apachectl start
./apachectl stop
./apachectl restart
./apachectl graceful
```
