#!/usr/bin/env python
#_*_coding:utf-8_*_
'''
�����ֵ���ʾ�û����Ե�½�ļ���������� ��shellԶ�̵�½������
'''

import os, sys

msg = """
\033[42;1mWelcom using baoleiji\033[0m;   
"""
print msg

hostdic = {
    '192.168.0.10':{'ip':'192.168.0.10','username':'yhzhao', 'password':'SunShine1001'},
    '192.168.0.14':{'ip':'192.168.0.14','username':'yhzhao', 'password':'SunShine1001'},
}


while True:
    for id, ip in enumerate(hostdic.keys(),1):
        print id, ip
    try:
        ipIndex = raw_input("please choose one host to login:")
        if ipIndex == 'quit':
            print 'Goodbye!'
            break
    except KeyboardInterrupt:continue
    except EOFError:continue
    if len(ipIndex) == 0:continue
    ipIndex = int(ipIndex)
    option = hostdic.values()[ipIndex-1]
    
    print '\033[32;1mGoing to connect %s\033[0m'%option['ip']
    os.system('python paramiko_demo.py %s %s %s'%(option['ip'],option['username'],option['password']))