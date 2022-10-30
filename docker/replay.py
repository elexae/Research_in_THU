import socks

class Client():
    def __init__(self, flow, proxyPort) -> None:
        self.flow = flow
        self.port = proxyPort

    def run(self, serverIp, serverPort) -> None:
        s = socks.socksocket()

        # 设置tor代理
        s.set_proxy(socks.SOCKS5, "localhost", self.port)
        s.connect((serverIp, serverPort))
        index = 0
        while index < len(self.flow):
            packet = self.flow[index]
            # 发送数据包
            while packet['direction'] == 'c2s':
                s.send('0' * packet['size'])
                index += 1
                packet = self.flow[index]
            # 接收数据包
            while packet['direction'] == 's2c':
                data = s.recv(4096)
        
class Server():
    def __init__(self) -> None:
        pass
