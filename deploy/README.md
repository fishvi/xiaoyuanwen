# Nginx + uWSGI + Daphne + supervisor
## 配置Centos 7  
1. 创建组和用户
```
[root@xiaoyuanwen ~]# groupadd xiaoyuanwen
[root@xiaoyuanwen ~]# useradd -m xiaoyuanwen -g xiaoyuanwen
[root@xiaoyuanwen ~]# passwd xiaoyuanwen

[xiaoyuanwen@xiaoyuanwen ~]$ chmod +x /home/xiaoyuanwen/  # 赋予执行权限
```  
2. 安装系统依赖  
```
[root@xiaoyuanwen ~]# yum -y update
[root@xiaoyuanwen ~]# yum -y install python-devel zlib-devel mysql-devel libffi-devel bzip2-devel openssl-devel java wget gcc
```  
3. 安装其它
```
[root@xiaoyuanwen ~]# yum -y install git redis nginx supervisor
```  
## 安装Python3
1. 下载编译
```
[root@xiaoyuanwen ~]# wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
[root@xiaoyuanwen ~]# tar -xvf Python-3.7.2.tar.xz
[root@xiaoyuanwen ~]# cd Python-3.7.2
[root@xiaoyuanwen ~]# ./configure --prefix=/usr/local/python3 --enable-optimizations
[root@xiaoyuanwen ~]# make
[root@xiaoyuanwen ~]# make install
```  
2. 创建软链接
```
[root@xiaoyuanwen ~]# ln -s /usr/local/python3/bin/python3 /usr/bin/python3
[root@xiaoyuanwen ~]# ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```  
3. 验证安装结果
```
[root@xiaoyuanwen ~]# python3 -V
Python 3.7.2
[root@xiaoyuanwen ~]# pip3 -V
pip 18.1 from /usr/local/python3/lib/python3.7/site-packages/pip (python 3.7)
[root@xiaoyuanwen ~]# whereis python3
python3: /usr/bin/python3 /usr/local/python3
[root@xiaoyuanwen ~]# whereis pip3
pip3: /usr/bin/pip3
```  
## 安装和配置MySQL
1. 下载
```
[root@xiaoyuanwen ~]# wget https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@xiaoyuanwen ~]# rpm -ivh mysql80-community-release-el7-2.noarch.rpm
[root@xiaoyuanwen ~]# yum -y install mysql-server
```
2. 启动服务
```
[root@xiaoyuanwen ~]# systemctl start mysqld
```
3. 创建数据库和用户  
*在/var/log/mysqld.log中找到临时密码, 其中Centos8默认密码为空*  
```
[root@xiaoyuanwen ~]# more /var/log/mysqld.log | grep temporary  # 在/var/log/mysqld.log中找到临时密码, 其中Centos8默认密码为空
[root@xiaoyuanwen ~]# mysql -u root -p
...
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '密码';  # 修改密码
mysql> create database xiaoyuanwen charset utf8;
mysql> create database test_xiaoyuanwen charset utf8;
mysql> create user 'xiaoyuanwen'@'localhost' identified by '密码';
mysql>
```  
4. 安全和权限设置
```
mysql> grant all on xiaoyuanwen.* to 'xiaoyuanwen'@'localhost';
mysql> grant all on test_xiaoyuanwen.* to 'xiaoyuanwen'@'localhost';
mysql> flush privileges;
mysql> exit
Bye
[root@xiaoyuanwen ~]#
```
## 安装Elasticsearch
```
[root@xiaoyuanwen ~]# su - xiaoyuanwen  # 切换到xiaoyuanwen用户，elasticsearch服务不能使用root用户运行
[xiaoyuanwen@xiaoyuanwen ~]$ wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.6/elasticsearch-2.4.6.tar.gz
[xiaoyuanwen@xiaoyuanwen ~]$ tar -xvf elasticsearch-2.4.6.tar.gz
```
## 上传代码
1. 创建logs
```
[xiaoyuanwen@xiaoyuanwen ~]$ cd xiaoyuanwen
[xiaoyuanwen@xiaoyuanwen xiaoyuanwen]$ mkdir logs
```
2. 安装依赖
```
[root@xiaoyuanwen ~]# pip3 install --upgrade pip
[root@xiaoyuanwen xiaoyuanwen]# pip3 install -r requirements.txt
```
3. 生成数据表
```
[xiaoyuanwen@xiaoyuanwen xiaoyuanwen]$ python3 manage.py makemigrations
[xiaoyuanwen@xiaoyuanwen xiaoyuanwen]$ python3 manage.py migrate
```
4. collect静态文件
```
[xiaoyuanwen@xiaoyuanwen xiaoyuanwen]$ python3 manage.py collectstatic
```
5. 压缩静态文件
```
[xiaoyuanwen@xiaoyuanwen xiaoyuanwen]$ python3 manage.py compress --force
```
## nginx+uwsgi+daphne+supervisor配置
详情见本目录下的各文件配置信息
## 启动服务并检查日志
1. 启动nginx和redis
```
[root@xiaoyuanwen deploy]# cp nginx.conf /etc/nginx/nginx.conf
[root@xiaoyuanwen ~]# systemctl start nginx
[root@xiaoyuanwen ~]# systemctl start redis
```
2. 启动supervisord
```
[root@xiaoyuanwen deploy]# cp uwsgi.ini /etc/
[root@xiaoyuanwen deploy]# cp xiaoyuanwen_* /etc/supervisord.d/
[root@xiaoyuanwen deploy]# systemctl start supervisord
[root@xiaoyuanwen deploy]# supervisorctl update
[root@xiaoyuanwen deploy]# supervisorctl reload
```
3. 验证
```
[xiaoyuanwen@xiaoyuanwen ~]$ ps -ef | grep python3  # 看uwsgi, daphe, celery进程是否都有
[xiaoyuanwen@xiaoyuanwen ~]$ curl http://localhost:9200  # 验证elasticsearch服务启动结果
```
4. 检查日志
```
[xiaoyuanwen@xiaoyuanwen ~]$ tail -5  xiaoyuanwen/logs/daphne.log
[root@xiaoyuanwen ~]# tail -5 xiaoyuanwen/logs/elasticsearch.log
[root@xiaoyuanwen ~]# tail -5 xiaoyuanwen/logs/celery.log
[root@xiaoyuanwen ~]# tail -5 xiaoyuanwen/logs/uwsgi.log
[root@xiaoyuanwen ~]# tail -5 /var/log/nginx/access.log
[root@xiaoyuanwen ~]# tail -5 /var/log/nginx/error.log
[root@xiaoyuanwen ~]# tail -10 /var/log/supervisor/supervisord.log
```
## 设置开机启动
```
[root@xiaoyuanwen ~]# systemctl enable redis nginx supervisord mysqld
```