---
title: scpwrapper小工具
date: 2019-11-09 20:05:00
tags: tool
---
# scpwrapper小工具

## scpwrapper源码
```
#!/usr/bin/bash

if [ "$1" == "get" ]
then
    scp -P 22 -r root@x.x.x.x:~/upload/$2 .
elif [ "$1" == "put" ]
then
    scp -P 22 -r $2 root@x.x.x.x:~/upload/
fi
```

## 用法
client端默认当前路径<br/>
server端默认~/upload/路径<br/>

./scpwrapper put tmp<br/>

将./tmp文件put到~/upload/tmp<br/>

./scpwrapper get dir<br/>

将~/upload/dir目录get到./dir目录下<br/>


## 免输入密码
client端<br/>
```
cd ~/.ssh/
ssh-keygen -t rsa
```
生成id_rsa, id_rsa.pub

server端
```
1. 将client端生成的id_rsa.pub拷贝到server端
./scpwrapper put ~/.ssh/id_rsa.pub
2. 追加客户端公钥到ssh的authorized_keys
cat ~/upload/id_rsa.pub >> ~/.ssh/authorized_keys
```
