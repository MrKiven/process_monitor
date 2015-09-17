#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'shenjialong'

l = [str(x) for x in xrange(10)]

l1 = [[1,2],[1,2,3],[1,2],[1,2,3]]

def chunks(list_data,m):
    return [list_data[i:i+m] for i in range(0,len(list_data),m)]
# print chunks(l,10)

f =  lambda l,m:[l[i:i+m] for i in xrange(0,len(l),m)]
for item_list in f(l1,2):
    for i_list in item_list:
        print i_list[1]
    print '++'