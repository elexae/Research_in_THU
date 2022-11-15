import os
import re
import dpkt
import pickle

rootDir = './results'
resultDirList = os.listDir(rootDir)
localIp = '172.31.109.129'

def compare(A, B):
    a = A.split('_')
    b = B.split('_')
    if int(a[0]) < int(b[0]):
        return True
    else:
        if int(a[1]) < int(b[1]):
            return True
        else:
            if int(a[2]) < int(b[2]):
                return True
            else:
                if int(a[3]) < int(b[3]):
                    return True
                else:
                    return False

def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def analysePcap(pcapFile, entryIps, time):
    feature = []
    with open(pcapFile, 'rb') as pf:
        pcap = dpkt.pcap.Reader(pf)
        for timestamp, buffer in pcap:
            if timestamp > time:
                break
            ethernet = dpkt.ethernet.Ethernet(buffer)
            if not isinstance(ethernet.data, dpkt.ip.IP):
                continue
            ip = ethernet.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue
            tcp = ip.data
            if not len(tcp.data):
                continue
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            if src == localIp and dst in entryIps:
                feature.append(-1)
            if src in entryIps and dst == localIp:
                feature.append(1)
    return feature

dataDir = './data'
createDir(dataDir)

for resultDir in resultDirList:
    flowDir = os.path.join(resultDir, 'inflow')
    logsDir = os.path.join(resultDir, 'logs')
    errorSitesFile = os.path.join(logsDir, 'errorSitesFULL.txt')
    entryIpFile = os.path.join(logsDir, 'entryIps.txt')
    timeElapsedFile = os.path.join(logsDir, 'timeElapsed.txt')
    errorSites = []
    info = {}
    flows = os.listDir(flowDir)
    indexs = sorted(list(map(lambda x : x[:-5], flows)), cmp=compare)
    with open(errorSitesFile, 'r') as ef:
        for line in ef.readlines():
            if len(line) == 0:
                continue
            errorSite = line.split(':')[0]
            errorSites.append(errorSite)
    reg = re.compile(r'^\[(?P<index>.*)\] (?P<onion_domain>.*) visit in (?P<time>.*),')
    with open(timeElapsed, 'r') as tf:
        for line in tf.readlines():
            regMatch = reg.match(line)
            regDic = regMatch.groupdict()
            if regDic['onion_domain'] not in errorSites:
                info[regDic['index']] = {'onion_domain' : regDic['onion_domain'], 'time' : float(regDic['time'])}
    p = 0
    with open(entryIpFile, 'r') as ef:
        for line in ef.readlines():
            entryIps = line.strip().split()
            index = indexs[p]
            p += 1
            if index not in info.keys():
                continue
            else:
                info[index]['entryIps'] = entryIps
    for k, v in info.items():
        index = k
        entryIps = v['entryIps']
        onion_domain = v['onion_domain']
        time = v['time']
        pcapFile = os.path.join(flowDir, index+'.pcap')
        feature = analysePcap(pcapFile, entryIps, time)
        outputDir = os.path.join(dataDir, onion_domain)
        createDir(outputDir)
        outputFile = os.path.join(outputDir, hash(onion_domain+''.join(entryIps)+str(time)))
        with open(outputFile, 'wb') as of:
            pickle.dump(feature, of)