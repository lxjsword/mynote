---
title: python subprocess使用总结
date: 2019-11-09 10:30:00
tags: python
---
# subprocess.call()
```python
父进程等待子进程完成
返回退出信息(returncode，相当于exit code，见Linux进程基础)

import subprocess
out = subprocess.call("ls -l", shell=True)
```


```python
Popen对象创建后，主程序不会自动等待子进程完成。我们必须调用对象的wait()方法，父进程才会等待 (也就是阻塞block)

import subprocess
child = subprocess.Popen(["ping","-c","5","www.google.com"])
child.wait()
print("parent process")
```


```python
子进程的文本流控制
(沿用child子进程) 子进程的标准输入，标准输出和标准错误也可以通过如下属性表示:

child.stdin

child.stdout

child.stderr
```
 
```python
我们可以在Popen()建立子进程的时候改变标准输入、标准输出和标准错误，并可以利用subprocess.PIPE将多个子进程的输入和输出连接在一起，构成管道(pipe):

import subprocess
child1 = subprocess.Popen(["ls","-l"], stdout=subprocess.PIPE)
child2 = subprocess.Popen(["wc"], stdin=child1.stdout,stdout=subprocess.PIPE)
out = child2.communicate()
print(out)
subprocess.PIPE实际上为文本流提供一个缓存区。child1的stdout将文本输出到缓存区，随后child2的stdin从该PIPE中将文本读取走。child2的输出文本也被存放在PIPE中，直到communicate()方法从PIPE中读取出PIPE中的文本。

要注意的是，communicate()是Popen对象的一个方法，该方法会阻塞父进程，直到子进程完成。
```

```python
我们还可以利用communicate()方法来使用PIPE给子进程输入:

import subprocess
child = subprocess.Popen(["cat"], stdin=subprocess.PIPE)
child.communicate("vamei")
我们启动子进程之后，cat会等待输入，直到我们用communicate()输入"vamei"。


self.p = subprocess.Popen(os.path.join(CommMan.COMMLIB_PATH, "EmuGetCapture.exe"), stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, shell=True, universal_newlines=True)
self.p.stdin.write("1\n")
self.p.stdin.flush()
self.p.stdout.readline()
```