import datetime
import subprocess
import os

# 控制tcpdump抓包
devnull = open(os.devnull, "w")

def catchFlow(ctx, pcapFile):
    t = ctx["interval"]
    logDir = os.path.join(ctx['logDir'], 'flowCatch')
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    logFile = logDir + '/' + 'test'
    cmd = 'timeout {} tcpdump -nn -i {} -w {}'.format(t, ctx['network'].NicName, pcapFile)
    with open(logFile, 'w') as fi: 
        return subprocess.Popen(cmd, stdout=fi, stderr= fi, shell=True)