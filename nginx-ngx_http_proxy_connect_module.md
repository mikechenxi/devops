# nginx 使用 ngx_http_proxy_connect_module 模块配置 http 正向代理

[TOC]

---

> 工作目录目录为 /app

## 1.安装依赖

```
    yum install gc gcc gcc-c++ pcre-devel zlib-devel openssl-devel patch
```

## 2.下载 nginx、ngx_http_proxy_connect_module 并解压

> master.zip 解压后文件夹为 ngx_http_proxy_connect_module-master

```
  wget https://nginx.org/download/nginx-1.12.2.tar.gz
  wget https://github.com/chobits/ngx_http_proxy_connect_module/archive/master.zip
  tar -xzvf nginx-1.12.2.tar.gz
  unzip master.zip
```

## 3.对 nginx 打 ngx_http_proxy_connect_module-master 补丁

```
  patch -d /app/nginx-1.12.2 -p1 </app/ngx_http_proxy_connect_module-master/patch/proxy_connect.patch
```

## 4.配置 nginx 

```
  cd /app/nginx-1.12.2
  ./configure --prefix=/app/nginx --with-http_ssl_module --add-module=/app/ngx_http_proxy_connect_module-master
```

## 5.编译、安装 nginx

```
  make
  make install
```

## 6.查看当前 nginx 的编译配置清单

```  
  /app/nginx/sbin/nginx -V
```

  显示如下
  
```
  nginx version: nginx/1.12.2
  built by gcc 4.8.5 20150623 (Red Hat 4.8.5-11) (GCC) 
  built with OpenSSL 1.0.1e-fips 11 Feb 2013
  TLS SNI support enabled
  configure arguments: --prefix=/app/nginx --with-http_ssl_module --add-module=/app/ngx_http_proxy_connect_module-master
```

## 7.配置代理

```
  server {
      listen       80;
      server_name  localhost;
      # dns resolver used by forward proxying
      resolver 10.204.24.1;
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
```

## 8.启动 nginx

```
  /app/nginx/sbin/nginx
```

## 9.测试代理是否生效

> 10.204.24.2 为 nginx 代理服务器

```
  curl https://github.com/ -v -x 10.204.24.2:80
```
