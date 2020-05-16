---
title: Ubuntu下搭建开发环境（二）
date: 2016-09-05 08:43:07
tags: 搭建环境
---
### vmware tools安装
``` bash
cp VMwareTools-9.6.5-2700074.tar.gz /opt
cd /opt
tar -zxvf VMwareTools-9.6.5-2700074.tar.gz /opt
cd vmware-tools-distrib
./vmware-install.pl 
```
<!-- more -->
### C++开发环境搭建
1. 先看一下g++装了否
``` bash
g++ --version
```
2. 因为要使用scons构建工具，会用到python, 看一下安装python否
``` bash
python --version
```
3. 安装scons
``` bash
cp scons-2.5.0.tar.gz /opt
cd /opt
tar -zxvf scons-2.5.0.tar.gz
cd scons-2.5.0/
./setup.py
```
4. 安装Sublime Text 2
``` bash
cd /opt
tar -jxvf Sublime\ Test\ 2.0.2.tar.bz2
cd Sublime\ Text\ 2
./sublime_text            //启动
```

### Java开发环境搭建
1. 先看一下是否已经安装了java
``` bash
java --version
```
2. 安装jdk
``` bash
cd /opt
sudo tar -zxvf jdk***.tar.gz
```
// 对profile进行配置
``` bash
vim /etc/profile
```
1）添加JAVA_HOME路径：
``` bash
export JAVA_HOME=/opt/jdk1.8.0_91
```
2)添加JRE路径
``` bash
export JRE_HOME=$JAVA_HOME/jre
```
3)配置CLASSPATH路径
``` bash
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
```
4）配置PATH路径
``` bash
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
```
    让刚才的配置生效
``` bash
source /etc/profile
```
    验证：
``` bash
java -version
```
3. 安装eclipse for java ee
``` bash
sudo tar -zxvf eclipse-jee****.tar.gz
        ./eclipse
```
4. 安装eclipse for c++
``` bash
sudo tar -zxvf eclipse-cpp***.tar.gz
    ./eclipse
```