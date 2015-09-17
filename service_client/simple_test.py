#!/usr/bin/python
# -*- coding:utf-8 -*-
from xmlrpclib import ServerProxy

__author__ = 'shenjialong'

if __name__ == '__main__':
    s = ServerProxy("http://192.168.80.52:3524")
    pids_list = s.get_pid_list()
    print '|'.join(pids_list)
    # print s.monitor(600,10,"work | grep -E '16884|16885|16886|16887|16888|16889|16890|16891|16892|16893|16894|16895|16896|16897|16898|16899|16900'")
