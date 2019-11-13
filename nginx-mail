# nginx 配置邮箱代理

[TOC]

---

> 工作目录目录为 /app

## 1.安装依赖

```
    yum install gc gcc gcc-c++ pcre-devel zlib-devel openssl-devel patch
```

## 2.下载 nginx 并解压

```
  wget https://nginx.org/download/nginx-1.12.2.tar.gz
  tar -xzvf nginx-1.12.2.tar.gz
```

## 3.配置 nginx 

```
  cd /app/nginx-1.12.2
  ./configure --prefix=/app/nginx --with-http_ssl_module --with-mail --with-stream
```

## 4.编译、安装 nginx

```
  make
  make install
```

## 5.配置代理

```
stream{
  server{
    listen 25;
    proxy_connect_timeout 5s;
    proxy_pass smtp.exmail.qq.com:25;
  }
}
```

## 5.启动 nginx

```
  /app/nginx/sbin/nginx
```

## 6.测试代理是否生效

> 10.204.24.2 为 nginx 代理服务器

发邮件时邮件服务器地址设置为 10.204.24.2 端口设置为 25
