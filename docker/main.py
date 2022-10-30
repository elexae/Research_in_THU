import utils
from flowCatch import catchFlow
from flowAnalysis import displayCircuitStatistic, pcap2flows
import time
import datetime

ctx = {}

# start private tor network
def startTorNetwork(config):
    pass

# read network information
def getNetworkInfo():
    network, nodeDict = utils.getInfo()
    ctx['network'] = network
    ctx['nodeDict'] = nodeDict

def init():
    ctx['interval'] = 10
    ctx['logDir'] = './logs'
    ctx['trafficDir'] = './pcap'

if __name__ == '__main__':
    # startTorNetwork()
    init()
    getNetworkInfo()

    client = ctx['nodeDict']['role']['CLIENT']
    circuits = utils.listCircuits(client, ctx)

    ntime = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    pcapFile = '{}/{}.pcap'.format(ctx['trafficDir'], ntime)
    catchFlow(ctx, pcapFile)

    time.sleep(15)
    ctx['flows'] = pcap2flows(pcapFile, ctx)
    for _, circuit in circuits.items():
        displayCircuitStatistic(circuit, ctx)