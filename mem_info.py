#!/usr/bin/env python3
import subprocess
import time
import os
import sys

OUTPUT_PATH = os.path.join(os.getcwd(),'mem_info.txt')
PERIOD_TIME = 1 #sec
TOTAL_TIME  = 60 #sec
USE_FIELD = 'MemTotal', 'MemFree', 'MemAvailable'
MEM_TOTAL = 0
MEM_FREE  = 0
MEM_AVAIL = 0

def bash_cmd(cmd: str):
    proc = subprocess.Popen(cmd, shell=True, executable="/bin/bash", \
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)

    ret = proc.communicate()
    if not proc.returncode:
        return (0,ret[0])
    else:
        return (proc.returncode, ret[1])

class Profiler():
    def __init__ (self):
        self.tool = 'cat /proc/meminfo'
        self.period = PERIOD_TIME #sec
        self.loop = TOTAL_TIME
        self.output_path = OUTPUT_PATH

    def _start(self):
        with open(self.output_path, "a") as o_fp:
            for i in (range(self.loop)):
                r_code, std = bash_cmd(self.tool)
                if not r_code:
                    self.strProcess(std) 
                    o_fp.write(std)
                    o_fp.write('\n')
                else:
                    print("ret code: %d" % r_code)
                    print(std)
                    sys.exit(r_code)
                if self.period != 0:
                    time.sleep(self.period)

    def strProcess(self,stdout):
        global MEM_TOTAL, MEM_FREE, MEM_AVAIL
        std_lines=stdout.split('\n')
        for raw_line in (std_lines):
            # Use Line by Line
            line = raw_line.split(':') 
            if line[0] not in USE_FIELD:
                break
            field = line[0]
            description = line[1].strip().split()
            content = int(description[0])
            unit = description[-1]
            if field == 'MemTotal':
                MEM_TOTAL += content
            elif field == 'MemFree':
                MEM_FREE += content
            elif field == 'MemAvailable':
                MEM_AVAIL += content
        #debug

    def preProcess(self):
        global MEM_TOTAL, MEM_FREE, MEM_AVAIL, PERIOD_TIME, TOTAL_TIME
        # 1. Do remove cache data
        r_code, std = bash_cmd('echo 3 > /proc/sys/vm/drop_caches')
        print("ret code: %d" % r_code)
        print(std)
    
    def postProcess(self):
        global MEM_TOTAL, MEM_FREE, MEM_AVAIL, PERIOD_TIME, TOTAL_TIME
        print('----- Avg Periode %d sec, Total %d second-------' % (PERIOD_TIME,TOTAL_TIME))
        print('MEM_TOTAL(kB): %d ' % MEM_TOTAL)
        print('MEM_FREE(kB): %d' % MEM_FREE)
        print('MEM_AVAIL(kB): %d' % MEM_AVAIL)
        #print('MEM_USED(Percentage): %f' % ((1-(MEM_AVAIL/MEM_TOTAL))*100))
        print('MEM_TOTAL - MEM_FREE: %.2f' % (MEM_TOTAL - MEM_FREE))

if __name__ == '__main__':
    p1 = Profiler()
    p1.preProcess()
    p1._start()
    p1.postProcess()

