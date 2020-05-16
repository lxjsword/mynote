---
title: python网络编程架构
date: 2019-11-09 00:15:10
tags: python
---
# python网络编程架构
### zen_utils.py
```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse, socket, time

aphorisms = {
    b'Beautiful is better than?': b'Ugly.',
    b'Explicit is better than?': b'Implicit.',
    b'Simple is better than?': b'Complex.',
}

def get_answer(aphorism):
    return aphorisms.get(aphorism, b'Error: unknown zphorism')

def parse_command_line(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='Ip or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port(default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    return address

def create_srv_socket(address):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def accept_connections_forever(listener):
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        handle_coversation(sock, address)

def handle_coversation(sock, address):
    try:
        while True:
            handle_request(sock)
    except EOFError:
        # 并不是真正的异常
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()
        
def handle_request(sock):
    aphorism = recv_until(sock, b'?')
    answer = get_answer(aphorism)
    sock.sendall(answer)

def recv_until(socket, suffix):
    message = socket.recv(4096)
    if not message:
        raise EOFError('socket closed')
    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data

    return message

```

### srv_single.py
```
#!/usr/bin/python
# -*- coding= UTF-8 -*-

import zen_utils

if __name__ == '__main__':
    address = zen_utils.parse_command_line('simple single-threaded server')
    listener = zen_utils.create_srv_socket(address)
    zen_utils.accept_connections_forever(listener)
```

### srv_thread.py
```
#!/usr/bin/python
# -*- coding= UTF-8 -*-

import zen_utils
from threading import Thread

def start_threads(listener, workers=4):
    t = (listener, )
    for i in range(workers):
        Thread(target=zen_utils.accept_connections_forever, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
```

### srv_process.py
```
#!/usr/bin/python
# -*- coding= UTF-8 -*-

import zen_utils
import multiprocessing

def start_processes(listener, workers=4):
    t = (listener, )
    for i in range(workers):
        multiprocessing.Process(target=zen_utils.accept_connections_forever, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-process server')
    listener = zen_utils.create_srv_socket(address)
    start_processes(listener)
```

### srv_async.py
```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import select, zen_utils, multiprocessing

def all_events_forever(poll_object):
    while True:
        for fd, event in poll_object.poll():
            yield fd, event

def serve(listener):
    sockets = {listener.fileno(): listener}
    clientaddress = {}
    bytes_received = {}
    bytes_to_send = {}

    poll_object = select.poll()
    poll_object.register(listener, select.POLLIN)

    for fd, event in all_events_forever(poll_object):
        sock = sockets[fd]

        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = clientaddress.pop(sock)
            rb = bytes_received.pop(sock, b'')
            sb = bytes_to_send.pop(sock, b'')
            if rb:
                print('Client {} sent {} but then closed'.format(address, rb))
            if sb:
                print('Client {} closed before we sent {}'.format(address, sb))
            else:
                print('Client {} closed socket normally'.format(address))
            poll_object.unregister(fd)
            del sockets[fd]
        
        elif sock is listener:
            sock, address = sock.accept()
            print('Accepted connection form {}'.format(address))
            sock.setblocking(False)
            sockets[sock.fileno()] = sock
            clientaddress[sock] = address
            poll_object.register(sock, select.POLLIN)
        
        elif event & select.POLLIN:
            more_data = sock.recv(4096)
            if not more_data:
                sock.close()
                continue
            data = bytes_received.pop(sock, b'') + more_data
            if data.endswith(b'?'):
                bytes_to_send[sock] = zen_utils.get_answer(data)
                poll_object.modify(sock, select.POLLOUT)
            else:
                bytes_received[sock] = data

        elif event & select.POLLOUT:
            data = bytes_to_send.pop(sock)
            n = sock.send(data)
            if n < len(data):
                bytes_to_send[sock] = data[n:]
            else:
                poll_object.modify(sock, select.POLLIN)
                
                
def startmultiserve(listener, workers=4):
    t = (listener, )
    for i in range(workers):
        multiprocessing.Process(target=serve, args=t).start()


if __name__ == '__main__':
    address = zen_utils.parse_command_line('low-level async server')
    listener = zen_utils.create_srv_socket(address)
    # 单进程+异步
    # serve(listener)

    # 多进程+异步
    startmultiserve(listener)

```

### client.py
```
#!/usr/bin/python
# -*- coding= UTF-8 -*-

import argparse, random, socket, zen_utils, time

def client(address, cause_error=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    aphorisms = list(zen_utils.aphorisms)
    if cause_error:
        sock.sendall(zen_utils.aphorisms[0][-1])
        return
    for aphorism in random.sample(aphorisms, 3):
        sock.sendall(aphorism)
        print(aphorism, zen_utils.recv_until(sock, b'.'))
    time.sleep(10)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)
    
```