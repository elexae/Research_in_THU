from stem import CircStatus
from stem.control import Controller

# Network
class Network():
    def __init__(self, id, nicName, subnet, gateway):
        self.id = id
        self.nicName = nicName
        self.subnet = subnet
        self.gateway = gateway

# node in tor network
class Node():
    def __init__(self, id, ip, ipPrefixLen):
        self.id = id
        self.ip = ip
        self.ipPrefixLen = ipPrefixLen

class Client(Node):
    def __init__(self, id, ip, ipPrefixLen, ctlPort, ctlPassword, ):
        super(Client, self).__init__(id, ip, ipPrefixLen)
        self.ctlPort = ctlPort
        self.ctlPassword = ctlPassword

    def getCircuits(self):
        with Controller.from_port(port = ctlPort) as controller:
        controller.authenticate(password=self.ctlPassword)

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
