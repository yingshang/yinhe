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
