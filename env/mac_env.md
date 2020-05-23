---
title: mac环境开发环境搭建
date: 2020-05-19 22:56:35
tags: 搭建环境
---
## ssh配置
```
# .ssh/config
# 支持会话复制，不用每次输入密码
host *
ControlMaster auto
ControlPath ~/.ssh/master-%r@%h:%p

Host xxx
  HostName xxx.xxx.com
  Port xxx
  User ryanxjli
  # 保持连接，防掉线
  ServerAliveInterval 10

Host cvm
  HostName xxx.xxx.xxx.xxx
  Port xxx
  User ryanxjli
  # 保持连接，防掉线
  ServerAliveInterval 10
  # 免密登陆
  IdentityFile /Users/ryanxjli/.ssh/id_rsa

Host homexxx
  HostName xxx.mnet2.com
  Port xxx
  User ryanxjli
  # 配置代理，使用corkscrew
  ProxyCommand /usr/local/bin/corkscrew 127.0.0.1 12679 %h %p
  # 保持连接，防掉线
  ServerAliveInterval 10

Host homecvm
  HostName xxx.xxx.xxx.xxx
  Port 36000
  User ryanxjli
  # 配置代理，使用corkscrew
  ProxyCommand /usr/local/bin/corkscrew 127.0.0.1 12679 %h %p
  # 保持连接，防掉线
  ServerAliveInterval 10
  # 免密登陆
  IdentityFile /Users/ryanxjli/.ssh/id_rsa
```

## 防治锁屏断开网络
节能->电池->去除勾选如果可能，使硬盘进入睡眠
节能->电源适配器->去除勾选如果可能，使硬盘进入睡眠 and 勾选如果显示器关闭时， 防止电脑自动进入睡眠

## 终端用iterm2+zsh
chsh /bin/zsh
.zshrc配置如下
```
# 走代理翻墙
export http_proxy=http://127.0.0.1:12639
export https_proxy=http://127.0.0.1:12639

# HomeBrew
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export PATH="/usr/local/bin:$PATH"
export PATH="/usr/local/sbin:$PATH"
# HomeBrew END

# 自定义
alias ll="ls -al"
# 公司
alias cvm="ssh cvm"
alias xxx="ssh xxx"
# 家里
alias homecvm="ssh homecvm"
alias homexxx="ssh homexxx"
```

## 安装Miniconda3