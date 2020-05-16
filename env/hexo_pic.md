---
title: hexo博客使用本地图片
date: 2016-09-04 16:14:31
tags: 搭建环境
---
### 环境配置
1. 首先修改_config.yml中的post_asset_golder属性。
``` bash
post_asset_floder: true
```
2. 在博客所在目录，执行
``` bash
npm install https://github.com/CodeFalling/hexo-asset-image --save
```
<!-- more -->
### 使用本地图片
1. 在source下添加存放图片的目录images
2. 使用时只用在代码中添加：
``` bash
![图片1](/images/title/p1.jpg)
```

