---
title: 安装配置hexo
date: 2016-09-04 16:14:31
tags: 搭建环境
---

### 必需的安装包下载与安装
1. 安装git或者github(必需)
2. 安装TortoiseGit和相应的语言包
3. 安装node.js(必需)v6.2.0
4. 安装markdown编辑器Haroopad
<!-- more -->
### 安装hexo
``` bash
npm install hexo-cli -g
```
### 初始化blog目录
``` bash
hexo init blog
```
### 新建一篇文章
``` bash
hexo new "安装配置hexo"
```
### 根据markdown文件生成静态网页
``` bash
hexo generate | hexo g
```
### 启动本地服务，在localhost:4000查看效果
```bash
hexo server | hexo s
```
### 部署到github服务器
到博客目录下修改_config.yml文件
``` bash
deploy:
    type: git
    repo: https://github.com/lxjsword/lxjsword.github.io.git
```
部署
``` bash
hexo deploy | hexo d
```
### 每次编写新的博客后，快捷生成部署
``` bash
hexo d -g
```
参考：[http://smile-leaf-language.github.io/](http://smile-leaf-language.github.io/)