import docker
import json

dockerClient = docker.from_env()
client = docker.APIClient(base_url='unix://var/run/docker.sock')

for container in dockerClient.containers.list():
    print(json.dumps(client.inspect_container(container.id), indent=4))
    break