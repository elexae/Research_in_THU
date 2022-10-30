import dpkt
import socket

def getNodePairs(circuit):
    nodePairs = []
    for i in range(len(circuit)-1):
        nodePairs.append([circuit[i], circuit[i+1]])
    return nodePairs

def pcap2flows(pcapFile, ctx):
    flows = {}
    with open(pcapFile, 'rb') as pf:
        pcap = dpkt.pcap.Reader(pf)
        for timestamp, buffer in pcap:
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
            k = "{}_{}".format(src, dst) if src < dst else "{}_{}".format(dst, src)
            # 选择需要保留的包信息
            if k not in flows.keys():
                flows[k] = []
            flows[k].append([src, dst, len(tcp.data)])
        return flows

def getCircuitStatistic(circuit, ctx):
    nodePairs = getNodePairs(circuit)
    statistic = {}
    for nodePair in nodePairs:
        nodeSrc, nodeDst = nodePair
        src, dst = nodeSrc.Ip, nodeDst.Ip
        k = "{}_{}".format(src, dst) if src < dst else "{}_{}".format(dst, src)
        statistic["{}_{}".format(src, dst)] = {"src2dst":{"size":0, "count":0}, "dst2src":{"size":0, "count":0}}
        if k not in ctx['flows'].keys():
            continue
        for packet in ctx['flows'][k]:
            if src == packet[0] and dst == packet[1]:
                statistic["{}_{}".format(src, dst)]["src2dst"]["count"] += 1
                statistic["{}_{}".format(src, dst)]["src2dst"]["size"] += packet[2]
            if src == packet[1] and dst == packet[0]:
                statistic["{}_{}".format(src, dst)]["dst2src"]["count"] += 1
                statistic["{}_{}".format(src, dst)]["dst2src"]["size"] += packet[2]
    return statistic

def displayCircuitStatistic(circuit, ctx):
    statistic = getCircuitStatistic(circuit, ctx)
    for i, node in enumerate(circuit):
        div = '+' if (i == len(circuit) - 1) else '|'
        address = node.Ip
        print("%s" % (address))

    for nodePair in getNodePairs(circuit):
        nodeSrc, nodeDst = nodePair
        src, dst = nodeSrc.Ip, nodeDst.Ip
        k = "{}_{}".format(src, dst)
        print("*"*16)
        print("from {} to {} : packet count {}, packet size {}.".format(src, dst, statistic[k]["src2dst"]["count"], statistic[k]["src2dst"]["size"]))
        print("from {} to {} : packet count {}, packet size {}.".format(dst, src, statistic[k]["dst2src"]["count"], statistic[k]["dst2src"]["size"]))
        print("*"*16)
