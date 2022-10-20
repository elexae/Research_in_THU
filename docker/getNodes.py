from http import client
import imp
import docker
from objects import Node

client = docker.from_env()

def filter(container):
    if "tornode" in container['Image']:
        return True
    return False

def getNodes(client):
    nodeList = []
    for container in client.containers.list():
        if filter(container):
