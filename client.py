#!/usr/bin/env python

import socket
import sys
import ssl

sl = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 27998
host_ip = socket.gethostbyname(str(sys.argv[2]))
wrappeds = sl.wrap_socket(s)
wrappeds.connect((host_ip, port))
hello = b'cs5700spring2021 HELLO '+str(sys.argv[3])+'\n'
wrappeds.send(hello)

while True:
    data = wrappeds.recv(16384)
    while not data.decode().endswith('\n'):
        data += wrappeds.recv(16384)
    expr = data.decode().replace('cs5700spring2021 EVAL ', '')
    print(expr)
    p=data.split()
    if p[1] == 'BYE':
        print p[1]
        break
    else:
        try:
            res = eval(str(expr))
            sts = b'cs5700spring2021 STATUS ' + str(res) + '\n'
            print(sts)
            wrappeds.send(sts)
        except ZeroDivisionError:
            err = b'cs5700spring2021 ERR #DIV/0' + '\n'
            print(err)
            wrappeds.send(err)
wrappeds.close()