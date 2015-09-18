#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
__author__ = 'shenjialong'


def get_pid_list(pid_command="ps aux|grep test.service |grep worker"):
    pid_list = []
    ret_text_list = os.popen(pid_command)
    for line in ret_text_list:
        pid_list.append(line.split()[1])
    return pid_list

if __name__ == '__main__':
    print '|'.join(get_pid_list())
