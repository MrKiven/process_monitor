#!/usr/bin/env python
# -*- coding: utf-8 -*-

import thriftpy
from thriftpy.rpc import make_server
pingpong_thrift = thriftpy.load("pingpong.thrift", module_name="pingpong_thrift")


class Dispatcher(object):
    def ping(self):
        return "pong"

server = make_server(pingpong_thrift.PingPong, Dispatcher(), '0.0.0.0', 6000)
server.serve()
