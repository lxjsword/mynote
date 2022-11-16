---
title: python多进程fork后，线程卡住
date: 2022-11-16 10:21:35
tags: python
---
## 问题描述
tornado框架后台服务接口请求大规模超时

## 问题定位
反复构造现场排查发现，出现问题时， 是启动后就发生了卡死， 说明是服务启动时就有问题

注意力还是瞄到了之前怀疑的后台线程这里（标注系统在启动时会起一个后台线程，然后才是服务进程的拉起）
![](/images/python/2.png)

之前也一直有这个后台线程，没有出现问题

反复试验，发现有后台线程的情况下，的确会有概率卡死， 去掉后台线程， 则不会

gdb attach问题进程， 发现主线程在正常epoll_wait, 线程池里的线程却出现了lock_wait_private卡死在这里
![](/images/python/3.png)

正常进程的子线程都是在do_futex_wait
![](/images/python/4.png)

pstack一下看下卡死调用， 发现是在getaddrinfo调用上， 再往下看没有找到有用的信息。
![](/images/python/5.png)

最终，定位到直接触发点是以下修改， 这里会通过socket上报网络日志
![](/images/python/6.png)


## 问题分析和解决
根据以往经验， 应该避免在多线程中的fork, 常会引发一些奇怪的问题， 包括线程消失， 内存泄露， 死锁。

唯一的例外是， fork出子进程后立刻调用exec函数，隔绝父子进程间资源访问，就像shell中执行命令其实都是exce出去子进程

以下这些博客有相关的分析

- https://www.cnblogs.com/liyuan989/p/4279210.html

- https://zhuanlan.zhihu.com/p/130873706

- https://github.com/redis/redis-rb/issues/436
- https://docs.newrelic.com/docs/apm/agents/ruby-agent/background-jobs/resque-instrumentation/



python官方文档描述如下

默认的fork模式， 官方文档也说明了， 多线程进程fork后是problematic的
forkserver模式， 每次fork都交给单线程的fork server生成新进程
![](/images/python/7.png)

tornado的网络服务模式是， 父进程listen socket fd后， fork出worker子进程继承父进程的listen fd进行accept， 父进程之后只负责管理子进程（比如子进程挂掉后自动生成新的worker进程），对外服务全部有worker进程处理

显然， 对于tornado框架使用的网络服务模型来说， 设置forkserver这种模式的话不可行，所以只能避免在父进程起多线程后再fork进程

最终解决方案：
单独起进程执行后台任务， 单独进程隔离了资源