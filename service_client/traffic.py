#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time,datetime
import sys

if len(sys.argv) > 2:
    INTERFACE = sys.argv[1]
    RUN_TIME = int(sys.argv[2])
else:
    print "缺少参数:","params: interface runtime"
    sys.exit(1)
    # INTERFACE = 'eth0'
STATS = []
print 'Interface:',INTERFACE


def	rx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in  ifstat:
        if INTERFACE in interface:
            stat = float(interface.split(":")[1].split()[0])
            STATS[0:] = [stat]


def	tx():
    ifstat = open('/proc/net/dev').readlines()
    for interface in  ifstat:
        if INTERFACE in interface:
            stat = float(interface.split()[9])
            STATS[1:] = [stat]

now = lambda is_str=True:time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) if str else datetime.datetime.now()

if __name__ == '__main__':
    f = open('./csv/' + INTERFACE + '_' + now() + '.csv','w')
    try:
        f.write(INTERFACE + "\n\n")
        f.write("In(KB)\t\t\tOut(KB)\n")
        result = []
        print	'In(KB)\t\t\tOut(KB)'
        start = time.time()
        rx()
        tx()
        while True:
            if (time.time()-start) > RUN_TIME:
                break
            time.sleep(1)
            rxstat_o = list(STATS)
            rx()
            tx()
            RX = float(STATS[0])
            RX_O = rxstat_o[0]
            TX = float(STATS[1])
            TX_O = rxstat_o[1]
            RX_RATE = round((RX - RX_O)/1024,3)
            TX_RATE = round((TX - TX_O)/1024,3)
            f.write(str(RX_RATE))
            f.write("\t\t\t")
            f.write(str(TX_RATE) + "\n")
            print RX_RATE ,'\t\t\t',TX_RATE
    except KeyboardInterrupt, e:
        print "\npyifstat exited"
    finally:
        f.close()
