---
title: celery残留redis不过期key问题解决
date: 2022-11-16 09:40:35
tags: python
---
## 问题描述：
celery运行一段时间， 做为消息队列的redis中会残留大key, xxx.reply.celery.pidbox, ttl设置为-1**永不过期**，导致redis内存一直上涨
![大key截图](/images/python/1.png)

## 问题解决：
网上搜到的解决方法
1. https://celery-users.narkive.com/dUQu2nLE/reply-celery-pidbox
2. https://github.com/celery/kombu/issues/294

最终参考了链接2的方法
```定期清理空闲key
red = app.backend.client
for key in red.scan_iter("*", 100000):
    if key.decode().startswith('_kombu'):
        continue
​
    if red.object('idletime', key) >= (24 * 7 * 3600):
        red.delete(key)
```
