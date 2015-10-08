#!/usr/bin/env python
# -*- coding: utf-8 -*-

import thriftpy
from thriftpy.rpc import make_client

pingpong_thrift = thriftpy.load("pingpong.thrift", module_name="pingpong_thrift")

client = make_client(pingpong_thrift.PingPong, '0.0.0.0', 6000)
print client.ping()
