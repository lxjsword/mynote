---
title: mysql安装
date: 2019-11-09 11:56:35
tags: tool
---
1. 添加mysql的yum源

rpm -Uvh https://repo.mysql.com//mysql80-community-release-el7-2.noarch.rpm
    
2. 查看yum源中所有Mysql版本

yum repolist all | grep mysql

3. 此时的最新版本是mysql8.0，把它禁用掉

yum-config-manager --disable mysql80-community

4. mysql5.7是我要安装的版本，启用mysql5.7

yum-config-manager --enable mysql57-community

5. 检查刚才的配置是否生效

yum repolist enabled | grep mysql

6. 开始安装

yum install mysql-community-server

7. 启动服务

service mysqld start

8. 启动完成之后检查mysql状态

service mysqld status

9. 查看临时密码

grep 'temporary password' /var/log/mysqld.log

10. 登录

mysql -uroot -p

11. 修改密码

set password for root@localhost=password('Lixj_19910629');