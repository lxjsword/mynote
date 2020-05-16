---
title: Windows下利用XX-Net翻墙
date: 2016-09-05 09:25:48
tags: 搭建环境
---
## Windows下利用XX-Net翻墙
总体来说，使用XX-Net科学上网，大致需要如下步骤：
1. 获取XX-Net
2. 设置和初始化：安装、设置完成后，如果无法翻墙，则需要等待后台程序扫描IP（10分钟到数小时）。
3. [可选]创建和使用自己的appid
4. 设置代理
5. [强烈建议]获取和配置可靠的浏览器（Firefox火狐浏览器，或Chrome谷歌浏览器），并使用代理切换插件。
6. 部署自己的服务器
<!-- more -->
下面分别介绍各个操作系统平台下的使用方法：

### Windows系统

双击 start.vbs或者start.bat启动。
Win7/8/10：将提示请求管理员权限（出于安装CA证书的需要）。请点击同意。
启动完毕后，将弹出浏览器，访问 http://localhost:8085/ （配置页面简介）
右下角将出现托盘图标：点击可弹出上述的XX-Net配置页面, 右键可显示常用功能菜单。
第一次启动, 会提示在桌面建立快捷方式,可根据自己需要选择。
推荐使用Chrome浏览器, 安装SwichySharp, 可在XX-Net目录中的SwitchySharp文件夹下找到插件和配置文件。
也可以选择使用Firefox（火狐）浏览器。需手动导入证书
启动失败，请关闭后双击start.bat再次启动程序，把日志发到bug反馈区

WinXP，需要破解tcp连接数，推荐使用tcp-z
Win8，win10 的APP，需要使用：https://loopback.codeplex.com/
Windows Server 2008，需要安装 Visual C++ 2008 Redistributable - x86
针对两种常用浏览器，分别有详细的新手图文教程：使用Firefox浏览器、使用Chrome浏览器


来源： https://github.com/XX-net/XX-Net/wiki/How-to-use
