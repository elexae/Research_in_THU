def extBidFlow(node1, node2, flow):
    eFlow = []
    for packet in flow:
        if packet['src'] == node1.ip and packet['dst'] == node2.ip:
            eFlow.append(packet)
        if packet['src'] == node2.ip and packet['dst'] == node1.ip:
            eFlow.append(packet)
    return eFlow

def extDireFlow(node1, node2, flow):
    eFlow = []
    for packet in flow:
        if packet['src'] == node1.ip and packet['dst'] == node2.ip:
            eFlow.append(packet)
    return eFlow

def extOutFlow(node, flow):
    eFlow = []
    for packet in flow:
        if packet['src'] == node.ip:
            eFlow.append(packet)
    return eFlow
