---
title: python pdb调试
date: 2019-11-08 15:56:10
tags: python
---
1. python pdb调试

```python
python -m pdb example.py

使用调试命令调试
```

2. diango pdb调试

```python
需要调试处

import pdb

pdb.set_trace()

运行django, python manage.py runserver

浏览器访问相应url, 进入断点处
```

3. 多进程远程调试

```python
rm_pdb.py

#!/usr/bin/env python

import socket
import sys
import threading
import pdb as _pdb


def server(addr='localhost', port=18964):
def __output(conn):
while True:
try:
                data = conn.recv(1024)
if not data: break
                sys.stdout.write(data)
                sys.stdout.flush()
except socket.error:
print "Connection close."
                break
            except:
break

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((addr, port))
    sock.listen(1)

print "Remote Pdb listening at %s:%d\n" % (addr, port)

try:
        conn, addr = sock.accept()
except KeyboardInterrupt:
        sys.exit(0)

print "Connect from %s\n" % str(addr)

    threading.Thread(target=__output, args=(conn,)).start()

try:
while 1:
            i = sys.stdin.readline()
            conn.sendall(i)
except socket.error:
print "Connection close."
    finally:
        conn.close()


def pdb(addr='localhost', port=18964):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))

return _pdb.Pdb(stdin=sock.makefile('r+', 0), stdout=sock.makefile('w+', 0))
```

```python
multiprocess_debug.py
#!/usr/bin/python

import multiprocessing
import pdb
import rm_pdb

def child_process():
print "Child-Process"
    rm_pdb.pdb().set_trace()
var = "debug me!"

def main_process():
print "Parent-Process"
    p = multiprocessing.Process(target = child_process)
    p.start()
    pdb.set_trace()
var = "debug me!"
    p.join()

if __name__ == "__main__":
    main_process()
运行
1. 先运行调试服务器python -c "import rm_pdb; rm_pdb.server()"
2. 运行需要调试的程序python multiprocess_debug.py
```
