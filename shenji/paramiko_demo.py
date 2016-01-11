#!/usr/bin/env python
#_*_coding:utf-8_*_
'''
SSHÔ¶³ÌµÇÂ½µ÷ÓÃ
'''

import os,sys,paramiko,time,multiprocessing
import interactive
ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
try:
    port = sys.argv[4]
except IndexError:
    port = 22

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, port, username, password)

channel = ssh.invoke_shell()
interactive.interactive_shell(channel, ip, username)
channel.close()
ssh.close()