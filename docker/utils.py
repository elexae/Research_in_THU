import docker
from objects import Node, Network
import subprocess
import re

def getInfo():
    dockerClient = docker.from_env()
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    # 获取docker网桥信息
    networkName = "tor"
    for n in dockerClient.networks.list():
        if networkName in n.name:
            networkInfo = client.inspect_network(n.id)
            subnet = networkInfo['IPAM']['Config'][0]["Subnet"]
            gateway = networkInfo['IPAM']['Config'][0]["Gateway"]
            nicIp = '/'.join([gateway, subnet.split('/')[1]])
            nicInfo = subprocess.getoutput("ip addr | grep {}".format(nicIp))
            pattern = re.compile(r'br-.*$')
            nicName = pattern.search(nicInfo).group()
            network = Network(n.id, nicName, subnet, gateway)

    nodeDict = {
        "role" : {},
        "ip" : {}
    }
    
    for container in dockerClient.containers.list():
        c = client.inspect_container(container.id)
        env = c['Config']['Env'] 
        for e in env:
            if "ROLE" in e:
                role = e[5:]
        image = c['Config']['Image']
        ip = c['NetworkSettings']['Networks']['private-tor-network_default']['IPAddress']
        ipPrefixLen = c['NetworkSettings']['Networks']['private-tor-network_default']['IPPrefixLen']
        if "tor" in image:
            node = Node(container.id, role, ip, ipPrefixLen)
            nodeDict["role"].setdefault(role, []).append(node)
            nodeDict["ip"].setdefault(node.Ip, node)
        else:
            continue

    return network, nodeDict

from stem import CircStatus
from stem.control import Controller

def listCircuits(client, ctx):
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")

        circuits = {}
        for circ in sorted(controller.get_circuits()):
            if circ.status != CircStatus.BUILT:
                continue

            circuit = []
            for i, entry in enumerate(circ.path):
                div = '+' if (i == len(circ.path) - 1) else '|'
                fingerprint, nickname = entry

                desc = controller.get_network_status(fingerprint, None)
                address = desc.address if desc else 'unknown'

                circuit.append(ctx['nodeDict']['ip'][address] if address in ctx['nodeDict']['ip'].keys() else 'unknow')
            circuits[circ.id] = circuit
        return circuits