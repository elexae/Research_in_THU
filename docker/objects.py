# Network
class Network():
    def __init__(self, Id, NicName, Subnet, Gateway) -> None:
        self.Id = Id
        self.NicName = NicName
        self.Subnet = Subnet
        self.Gateway = Gateway

# node in tor network
class Node():
    def __init__(self, Id, Role, Ip, IpPrefixLen) -> None:
        self.Id = Id
        self.Role = Role
        self.Ip = Ip
        self.IpPrefixLen = IpPrefixLen