## download

```
curl https://raw.githubusercontent.com/mikechenxi/devops/main/ops/rinetd.tar.gz
```

## install

``` 
tar -xzvf rinetd.tar.gz
cd rinetd
make
make install
```

if error 'cannot create regular file ‘/usr/man/man8’: No such file or directory', create fold by 'mkdir -p /usr/man/man8'

## config

```
echo '0.0.0.0 25 smtp.exmail.qq.com 25' >> /etc/rinetd.conf
```

forward local port 25 to tencent exmail port 25

## start

```
rinetd -c /etc/rinetd
```
