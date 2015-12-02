#encoding: utf-8
'''
Created on 2015年12月1日

@author: lml
'''

import sys
import threading
sys.path.append("../")
sys.path.append("../../")
sys.path.append("/home/lml/webcrawler/webcrawler-nlp/crawler/")

import paramiko
import threading

def ssh2(ip,username,passwd,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
#           stdin.write("Y")   #简单交互，输入 ‘Y’ 
            out = stdout.readlines()
            #屏幕输出
            for o in out:
                print o,
        print '%s\tOK\n'%(ip)
        ssh.close()
    except :
        print '%s\tError\n'%(ip)


if __name__=='__main__':
    cmd = [
           'cd "/home/lml/webcrawler/webcrawler-nlp"',
            'echo "lml19870419" | git pull',
           'echo "lml19870419" | sudo -S bash /home/lml/webcrawler/webcrawler-nlp/crawler/sql_script/restartcrawler.sh'
           ]#你要执行的命令列表
    username = "lml"  #用户名
    passwd = "lml19870419"    #密码
    ip = "192.168.1.101"
    print "Begin......"
    ssh2(ip, username, passwd, cmd)


