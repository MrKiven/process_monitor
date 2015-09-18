#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import os
import sys
from isDigit import check_isDigit
import threading

__author__ = 'shenjialong'

'''
将保存cpu、mem数据的log文件画成图
the main pylot module
params : data path , save path ,cpu cores ,pic dpi
return : pic path
'''

# 锁
lock = threading.Lock()

F = lambda l, m: [l[i: i + m] for i in xrange(0, len(l), m)]


class PylotMain(object):

    def __init__(self, data_path, save_path, cpu_cores, dpi=100):
        self.data_path = data_path
        self.save_path = save_path
        self.cpu_cores = cpu_cores
        self.dpi = dpi

    def _get_data_list(self):
        cpu_core = 8
        worker_process = cpu_core * 2 + 1
        all_test = {}
        for path, dirs, files in os.walk(self.data_path):
            for file in files:
                one_test_cpu_list, one_test_mem_list = [], []
                if file.endswith("_K.log"):
                    with open(path + file, 'r') as f:
                        print file
                        lines = f.readlines()
                        new_lines = []
                        for line in lines:
                            line = line.rstrip('\n').split()
                            if not check_isDigit(line[8]) or not check_isDigit(line[9]):
                                continue
                            else:
                                new_lines.append(line)
                        for every_17_line_of_list in F(new_lines, worker_process):
                            every_17_cpu_usage, every_17_mem_usage = 0, 0
                            for every_line_of_list in every_17_line_of_list:
                                single_cpu, single_mem = float(every_line_of_list[8]), float(every_line_of_list[9])
                                every_17_cpu_usage += single_cpu
                                every_17_mem_usage += single_mem
                            one_test_cpu_list.append(every_17_cpu_usage / cpu_core)
                            one_test_mem_list.append(every_17_mem_usage)
                    all_test[file] = {
                        "cpu": one_test_cpu_list,
                        "mem": one_test_mem_list,
                    }
        # print all_test
        return all_test

    # 画图
    def draw_pic_and_save(self):
        global lock
        all_log = self._get_data_list()
        for one_log in all_log:
            # print log,data_type[log]
            lock.acquire()
            # print "拿锁..."
            cpu_data, mem_data = all_log[one_log]['cpu'], all_log[one_log]['mem']
            pic_name = one_log.split('.')[0]
            cpu_len, mem_len = len(cpu_data), len(mem_data)

            x1 = [i * 5 for i in xrange(cpu_len)]
            x2 = [i * 5 for i in xrange(mem_len)]
            y1 = cpu_data
            y2 = mem_data
            plt.title("CPU&MEM")
            plt.xlabel('time--seconds')
            plt.ylabel('avg CPU --%/MEM --KB')
            plt.ylim(0, 100)
            pic = plt.plot(x1, y1, x2, y2)
            plt.setp(pic, linewidth=0.4)
            plt.legend(pic, ['cpu', 'mem'], 'lower left')
            # plt.grid(True)
            plt.savefig(self.save_path + pic_name + '.png', dpi=self.dpi)
            plt.close()
            print "saved:" + pic_name + ".png in " + self.save_path
            lock.release()
            # print "释放锁..."


def cpu_stat():
    cpu = 0
    try:
        with open("/proc/cpuinfo") as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip('\n')
                if line.startswith('processor'):
                    cpu += 1
    except Exception:
        print '''
    warning:
        not linux system!!
        '''
    finally:
        return cpu


if __name__ == '__main__':
    if not len(sys.argv) == 4 and not len(sys.argv) == 3:
        print '''
    error :
        example : ./pic_generater.py data_path(目标路径) save_path(保存路径) [cpu核心数(可选)]
        '''
        sys.exit(1)
    data_path = sys.argv[1]
    save_path = sys.argv[2]
    cores = int(cpu_stat())
    if not cores:
        if len(sys.argv) == 3:
            print '''
        error :
            should use like :./pic_generater.py data_path(目标路径) save_path(保存路径) cpu核心数
            '''
            sys.exit(1)
        cores = int(sys.argv[3])
    print "cores:", cores
    p = PylotMain(data_path, save_path, cpu_cores=cores)
    p.draw_pic_and_save()
