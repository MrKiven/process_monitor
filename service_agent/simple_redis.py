#!/usr/bin/python
# -*- coding:utf-8 -*-
import redis
__author__ = 'shenjialong'

r = redis.Redis(host="192.168.80.25",port=6379)
print r.keys()
