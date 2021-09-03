# nginx 配置 http 正向代理、定向 http 正向代理、反向代理以及 email 代理


> 工作目录目录为 /home

## 1.安装依赖

```
    yum install gc gcc gcc-c++ pcre-devel zlib-devel openssl-devel patch
```

## 2.下载 nginx、ngx_http_proxy_connect_module 并解压(http正向代理)

> master.zip 解压后文件夹为 ngx_http_proxy_connect_module-master

```
  wget https://nginx.org/download/nginx-1.12.2.tar.gz
  wget https://github.com/chobits/ngx_http_proxy_connect_module/archive/master.zip
  tar -xzvf nginx-1.12.2.tar.gz
  unzip master.zip
```

## 3.对 nginx 打 ngx_http_proxy_connect_module-master 补丁

```
  patch -d /home/nginx-1.12.2 -p1 </home/ngx_http_proxy_connect_module-master/patch/proxy_connect.patch
```

## 4.配置 nginx 

```
  cd nginx-1.12.2
  ./configure --prefix=/app/nginx-1.12.2 --with-http_ssl_module --add-module=/home/ngx_http_proxy_connect_module-master
```

## 5.编译、安装 nginx

```
  make
  make install
```

## 6.查看当前 nginx 的编译配置清单

```  
  /app/nginx-1.12.2/sbin/nginx -V
```

  显示如下
  
```
  nginx version: nginx/1.12.2
  built by gcc 4.8.5 20150623 (Red Hat 4.8.5-11) (GCC) 
  built with OpenSSL 1.0.1e-fips 11 Feb 2013
  TLS SNI support enabled
  configure arguments: --prefix=/app/nginx --with-http_ssl_module --add-module=/app/ngx_http_proxy_connect_module-master
```

## 7.配置 http 正向代理

```
http {
  server {
    listen 80;
    server_name  localhost;
    # dns resolver used by forward proxying
    resolver xx.xx.xx.xx;  # dns
    # forward proxy for CONNECT request
    proxy_connect;
    proxy_connect_allow all;
    proxy_connect_connect_timeout 15s;
    proxy_connect_read_timeout 15s;
    proxy_connect_send_timeout 15s;
    # forward proxy for non-CONNECT request
    location / {
      proxy_pass http://$http_host;
      proxy_set_header Host $http_host;
    }
  }
}
```

## 8.配置定向 http 正向代理

```
http {
  server {
    listen  80;
    server_name xx.xx.com;
    location / {
      resolver xx.xx.xx.xx;  # dns
      proxy_pass https://qyapi.weixin.qq.com/;
    }
  }
}
```

## 9.配置 http 反向代理

```
http {
  server {
    listen  80;
    server_name xx.xx.com;
    rewrite ^(.*)$  https://$host$1 permanent;
  }

  server {
    listen 443;
    server_name  xx.xx.com;

    ssl   on;
    ssl_certificate      /app/nginx/conf/https/a.pem;
    ssl_certificate_key  /app/nginx/conf/https/a.key;
    ssl_session_timeout  5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers  HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM;
    ssl_prefer_server_ciphers   on;

    location =/ {
      rewrite ^(.*)$  https://$host/oa/main;
    }
    
    location /oa {
      proxy_pass http://xx.xx.xx.xx/oa;
      proxy_redirect  off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header REMOTE-HOST $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto  $scheme;
    }
  }
}
```

## 10.配置 email 代理

```
stream{
  server{
    listen 25;
    proxy_connect_timeout 5s;
    proxy_pass smtp.exmail.qq.com:25;
  }
  server{
    listen 465;
    proxy_connect_timeout 5s;
    proxy_pass smtp.exmail.qq.com:465;
  }
}
```

## 11.启动、快速停止、 正常停止、重新加载配置文件nginx

```
  /app/nginx-1.12.2/sbin/nginx
  /app/nginx-1.12.2/sbin/nginx -s stop
  /app/nginx-1.12.2/sbin/nginx -s quit
  /app/nginx-1.12.2/sbin/nginx -s reload
```

## 12.测试代理是否生效

> 10.204.24.2 为 nginx 代理服务器

### http

```
  curl https://github.com/ -v -x 10.204.24.2:88
```

### email

>发邮件时邮件服务器地址设置为 10.204.24.2 端口设置为 25
