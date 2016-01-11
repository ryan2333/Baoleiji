#!/usr/bin/env python
#_*_coding:utf-8_*_

'''
执行远程登陆服务器，并记录下用户执行的操作

'''

import socket
import sys, os, time
from paramiko.py3compat import u

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, ip, username):#传入参数IP 端口 用户名
    if has_termios:
        posix_shell(chan, ip, username) #传入参数IP 端口 用户名
    else:
        windows_shell(chan)


def posix_shell(chan, ip, username): #传入参数IP 端口 用户名
    import select
    
    oldtty = termios.tcgetattr(sys.stdin)
    f = file('/tmp/act.log', 'a+')
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        recods = ''
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                recods += x
                if x == '\r':
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                    msg = "ip:%-15susername:%-15sdate:%-25scmd:%s"%(ip, username, current_time, recods.replace('\r', ''))#传入参数IP 端口 用户名
                    msg = msg + os.linesep
                    f.write(msg)
                    f.flush()
                    recods = ''
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        f.close()
    
# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
        
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()
        
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
        
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass