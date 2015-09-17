#!/usr/bin/python
# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import os,sys
__author__ = 'shenjialong'

#
# 将 网络流量的 csv文件画成图
#

def analyse(csv_file):
    result = {}
    with open(csv_file) as f:
        lines = f.readlines()
        interface = lines[0].rstrip('\n')
        role = lines[2].rstrip('\n').split()
        result[interface] = {
            role[0]:[],
            role[1]:[]
        }
        for line in lines[3:]:
            every_line_list = line.rstrip('\n').split("\t\t\t")
            result[interface][role[0]].append(float(every_line_list[0]))
            result[interface][role[1]].append(float(every_line_list[1]))
    '''
    {
        'eth0':{
            'Out(KB)':[1,2,3,4,5,6....],
            'In(KB)':[1,2,3,4,5,6...]
        }
    }
    '''
    return result


def draw_pic_and_save(csv_file,target):
    data = analyse(csv_file)
    # file,ext = os.path.splitext(csv_file)
    file_name = os.path.basename(csv_file).split('.')[0]

    for device in data:
        title = device
        y1 = data[device]['Out(KB)']
        y2 = data[device]['In(KB)']
        x = [i for i in xrange(len(y1))]
        plt.title(title)
        plt.xlabel('time--seconds')
        plt.ylabel('NetIO--KB')
        pic = plt.plot(x,y1,x,y2)
        plt.setp(pic ,linewidth=0.4)
        plt.legend(pic,['Out','In'],'lower left')
        plt.savefig(target + file_name + '.png' ,dpi=100)
        plt.close()
        print "saved:" + file_name + ".png in " + target


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print '''
    error :
        example : ./traffic_analyse.py data_path(目标路径) save_path(保存路径)
        '''
        sys.exit(1)
    data_path = sys.argv[1]
    save_path = sys.argv[2]
    draw_pic_and_save(data_path,save_path)
