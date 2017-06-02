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

## 注意：使用centos不能抓取https数据包，原因不明，具体可以到这里了解
'''
https://github.com/mitmproxy/mitmproxy/issues/1608
'''
