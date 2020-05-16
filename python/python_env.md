---
title: python开发环境搭建
date: 2019-11-09 11:56:35
tags: python
---
1. 安装 Python2.7.5

2. 依赖包安装方式：

```bash
pip install -r requirements.txt

pip install gevent
```


1. 安装python2.7.10 32位
	
2. 安装并建立虚拟环境virtualenv
```
	pip install virtualenv
	# 指定按本地python版本， 不安装包建立虚拟环境
	virtualenv venv2.7-Scrapy -p /usr/local/bin/python --no-site-packages
	
	Cd py27_dj1.11.16/bin
	source activate
	
    pip install django==1.11.16
```
