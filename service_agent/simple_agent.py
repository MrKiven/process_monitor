#!/usr/bin/python
# -*- coding:utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os
import time
import datetime
import sys

__author__ = 'shenjialong'

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

RUNNING = True
LISTEN_SETTING = {
    "IP": "0.0.0.0",
    "PORT": 3524,
}


class Task(object):

    def __init__(self):
        logging.info("xmlrpc server start...")

    # 获取pid
    def get_pid_list(self, pid_command):
        if not pid_command:
            raise ValueError("{} cannt be empty")
        pid_list = []
        ret_text_list = os.popen(pid_command)
        for line in ret_text_list:
            pid_list.append(line.split()[1])
        logging.info(pid_list)
        return pid_list

    def monitor(self, how_long, interval, what):
        '''
           how_long -> 监控多长时间，秒 60
           interval -> 监控间隔时间，秒 1
           what -> 监控的进程
        '''
        self.how_long, self.interval, self.what = how_long, interval, what
        # 多少次
        _n = how_long / interval
        log_time, log_path = self._now(), "./log/"
        if os.path.exists(log_path):
            pass
        else:
            os.mkdir(log_path)

        self._cmd = "nohup top -b -d {} -n {} | grep {} >> {} &"\
            .format(interval, _n, what, log_path + log_time + "_K.log")
        logging.info("monitor start... ,lasts %s", self.how_long)
        print self._cmd
        os.popen(self._cmd)

    # private function
    def _now(self, is_str=True):
        if str:  # return string type
            return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        else:  # return datetime.datetime type
            return datetime.datetime.now()

    # use test
    def ping(self):
        return True

    def stop(self):
        global RUNNING
        RUNNING = False
        logging.info("xmlrpc server stop...")


if __name__ == '__main__':
    s = SimpleXMLRPCServer((LISTEN_SETTING['IP'], LISTEN_SETTING['PORT']), allow_none=True)
    s.register_instance(Task())
    logging.info("listening on port {}...".format(LISTEN_SETTING['PORT']))
    while RUNNING:
        try:
            s.handle_request()
        except KeyboardInterrupt:
            logging.info("xmlrpc server stop...")
            sys.exit(1)
    # s.serve_forever()
