import datetime

# 控制tcpdump抓包
devnull = open(os.devnull, "w")

def startTcpdump(pcapFile, logFile, nic):
    cmd = 'tcpdump -nn -i {} -G 60 -w pcap/%Y_%m_%d_%H_%M_%S.pcap'.format(nic)
    with open(logFile, 'w') as fi: 
        return subprocess.Popen(cmd, stdout=fi, stderr= fi, shell=True)

def killTcpdump(command):
    proc = subprocess.Popen(command, stdout=devnull, stderr=subprocess.STDOUT)
    proc.wait()
    proc.terminate()

def catchFlow():
    
    