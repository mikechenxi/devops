# apache 使用 mod_jk 模块配置 AJP 反向代理

> 工作目录目录为 /app/apache

## 安装依赖包 

```
yum install  gcc-c++
```

## 下载软件 httpd、apr、apr-util、pcre、mod_jk

```
wget http://mirrors.tuna.tsinghua.edu.cn/apache//apr/apr-1.7.0.tar.gz
wget http://mirrors.tuna.tsinghua.edu.cn/apache//apr/apr-util-1.6.1.tar.gz
wget ftp://ftp.pcre.org/pub/pcre/pcre-8.43.tar.gz
wget http://mirrors.tuna.tsinghua.edu.cn/apache//httpd/httpd-2.4.41.tar.gz
wget http://mirror.bit.edu.cn/apache/tomcat/tomcat-connectors/jk/tomcat-connectors-1.2.46-src.tar.gz
tar -xzvf apr-1.7.0.tar.gz
tar -xzvf apr-util-1.6.1.tar.gz
tar -xzvf pcre-8.43.tar.gz
tar -xzvf httpd-2.4.41.tar.gz
tar -xzvf tomcat-connectors-1.2.46-src.tar.gz
```

## 安装软件

安装 apr

```
cd apr-1.7.0
./configure --prefix=/app/apache/apr
make
make install
```

安装 apr-util

```
cd apr-util-1.6.1
./configure --prefix=/app/apache/apr-util --with-apr=/app/apache/apr/bin/apr-1-config
make
make install
```

安装 pcre

```
cd pcre-8.43
./configure --prefix=/app/apache/pcre --with-apr=/app/apache/apr/bin/apr-1-config
make
make install
```

如果安装 apr-util 提示 expat.h: No such file or directory，需要安装expat-devel

在线安装 expat-devel

```
yum install expat-devel
```

离线安装 expat-devel

```
wget https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/expat/2.0.1-7.2/expat_2.0.1.orig.tar.gz
tar -xzvf expat_2.0.1.orig.tar.gz
cd expat_2.0.1.orig.tar.gz
./configure
make
make install
```

安装 apache

```
cd httpd-2.4.41
./configure --prefix=/app/apache/httpd --with-pcre=/app/apache/pcre --with-apr=/app/apache/apr --with-apr-util=/app/apache/apr-util
make
make install
```

安装 mod_jk

```
cd tomcat-connectors-1.2.42-src/native/
./configure --with-apxs=/app/apache/httpd/bin/apxs
make
make install
```

## 配置 apache

编辑 /app/apache/httpd/conf/httpd.conf, 末尾加上 

```
LoadModule deflate_module modules/mod_deflate.so

Include conf/mod_jk.conf
AddOutputFilterByType DEFLATE text/html text/plain text/xml
```

/app/apache/httpd/conf/ 目录新建 mod_jk.conf, 内容如下

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
JkRequestLogFormat "%w %V %T"
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

/app/apache/httpd/conf/ 目录新建 workers.properties, 内容如下(192.168.189.133为tomcat所在服务器)

```
worker.list = controller,status 
worker.status.type=status
worker.controller.type=lb

worker.controller.balance_workers=OAapp

worker.controller.sticky_session=1
worker.controller.sticky_session_force=0

worker.OAapp.port=8009
worker.OAapp.host=192.168.189.133
worker.OAapp.type=ajp13
worker.OAapp.lbfactor=1
worker.OAapp.retries=3
```

/app/apache/httpd/conf/ 目录新建 uriworkermap.properties, 内容如下

```
/*=controller
/jkstatus= status
```

## 启动apache

```
cd /app/apache/httpd/bin
./apachectl
```
