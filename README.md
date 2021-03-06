# yinhe-Passive Vulnerability Scan

银河是一款基于代理抓包和流量监控的被动式扫描系统
## 安装依赖
### ubuntu
安装环境
```
apt-get install -y python-pip python-dev build-essential libmysqlclient-dev libssl-dev mysql-server libxml2-dev libxslt1-dev
pip install --upgrade pip
```
下载源码
```
cd /opt/
git clone https://github.com/yingshang/yinhe.git
pip  install -r requirements.txt
```
创建数据库
```
mysql> create database yinhe;
Query OK, 1 row affected (0.00 sec)

```

启动服务
```
root@ubuntu:/opt/yinhe# python manage.py runserver 0.0.0.0:8000
Performing system checks...

System check identified no issues (0 silenced).
June 02, 2017 - 16:41:40
Django version 1.9.2, using settings 'yinhe.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.
```
打开网页127.0.0.1:8000/capture,直接监听端口就可以
数据包
![](https://github.com/yingshang/yinhe/blob/master/docs/images/1.png)
![](https://github.com/yingshang/yinhe/blob/master/docs/images/2.png)


然后对抓取到数据包进行测试，启动sqlmapapi
```
[root@localhost sqlmap]# python sqlmapapi.py -s
[17:06:54] [INFO] Running REST-JSON API server at '127.0.0.1:8775'..
[17:06:54] [INFO] Admin ID: b42d7d50acd25053b2f6ea5e3c839095
[17:06:54] [DEBUG] IPC database: '/tmp/sqlmapipc-yyzZdy'
[17:06:54] [DEBUG] REST-JSON API server connected to IPC database
[17:06:54] [DEBUG] Using adapter 'wsgiref' to run bottle
```
使用dvwa进行测试
运行127.0.0.1:8000/run,后台就会自动对数据包进行测试
http://127.0.0.1:8000/sqli/       #更新漏洞状态
http://127.0.0.1:8000/sqli_detail/fa4b6a8aec1c11db    #显示漏洞情况
![](https://github.com/yingshang/yinhe/blob/master/docs/images/3.bmp)

## 已知漏洞
1.
### 注意：使用centos不能抓取https数据包，原因不明，具体可以到这里了解
```
https://github.com/mitmproxy/mitmproxy/issues/1608
```
2.
使用0.0.0.0抓取局域网的数据包，抓不了，用127.0.0.1访问就可以抓包，但是都可以抓包外网的数据包
## ChangeLog
2017.6.2  write reports


python manage.py celery -A yinhe worker -l info --beat