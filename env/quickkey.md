---
title: tmux,nvim常用快捷键
date: 2021-04-10 11:50:57
tags: 搭建环境
---

1. vim快捷键
```bash
prefix为space

# nerdtree快捷键
prefix+n 打开左边目录菜单
o 打开文件
s 左右分割打开文件
t tab页打开文件

# leaderf快捷键
prefix+ff 搜索文件
prefix+rg 搜索关键字
prefix+gf 搜索选中关键字
#leaderf+gtags
prefix+fr 跳转到引用
prefix+fd 跳转到定义
prefix+fn 跳转到下一处
prefix+fp 跳转到上一处

# coc.nvim快捷键
prefix+cc 注释
prefix+cu 取消注释
prefix+cf 格式化代码

# gutentas快捷键
ctrl+] 跳转到定义
ctrl+o 跳转到上次页面

# 复制粘贴
"+y 复制到系统剪贴板
'''

2. tmux快捷键
'''bash
tmux ls 显示会话
tmux a attach会话

# prefix为ctrl+a
prefix+s 显示所有会话
prefix+窗口编号 窗口间跳动
prefix+方向键 窗格间移动
prefix按住+方向键 窗格大小调整
'''
