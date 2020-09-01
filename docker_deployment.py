import docker
import machine
import subprocess
import threading
import os

machine = machine.Machine()
client = docker.client.from_env()
swarm = client.swarm
containers = client.containers
nodes = client.nodes
images = client.images

def remove_all_machines():
        try:
            for mach in machine.ls():
                name = mach['Name']
                print(f"Removing docker machine {name}")
                result = subprocess.run(["docker-machine", "rm", name, "--force"], capture_output=True)
            return True
        except:
            return False

def get_join_token(role):
    result = subprocess.run(["docker", "swarm", "join-token", role], capture_output=True)
    string = result.stdout
    return result.stdout.decode('utf-8').split("    ")[1][:-2]

def new_swarm():
    try:
        print("Initializing new swarm")
        manager = swarm.init()
    except:
        swarm.leave(force=True)
        manager = swarm.init()
    return manager


def build_machine(machine_name):
    node = machine.create(machine_name, xarg=["--virtualbox-memory=1024"])
    return node


def build_machines(machines):
    for machine_name in machines:
        print(f"Building machine {machine_name}")
        build_machine(machine_name)

    return machine.ls()

def build_containers(name):
    print(f"Switching to machine environment for name {name}")
    os.system(f"eval $(docker-machine env {machine['Name']})")

    result = os.system(f"docker stack deploy --compose-file machine_compose/{name}.yml {name}")
    return result

def build_image(service, push=False):
    print(f"Building {service}")
    if service == "node_base":
        image = images.build(path=".", dockerfile="./docker/node/node_base.Dockerfile", tag="node_base")
    if service == "newsblur_base":
        image = images.build(path=".", dockerfile="./docker/newsblur_base_image.Dockerfile", tag="newsblur_base") 
    elif service == "haproxy":
        image =  images.build(path=".", dockerfile="./docker/haproxy/Dockerfile", tag="haproxy")
    else:
        print("Service not found")
    print(f"Built {image}")
    print("Pushing image")
    repository = f"jmath1/{service}"
    if push:
        print("Pushing image")
        image.push(repository, tag='')
        

class DockerCluster():

    def __init__(self, name, environment="dev", restart_swarm=False):
        self.name = name
        
        if restart_swarm:
            remove_all_machines()
            swarm_manager = new_swarm()
            

        if environment == "dev":
            """
            if dev, use swarm with docker machine. Otherwise, use digital ocean
            """
            manager_join_token_command = get_join_token(role="manager")
            worker_join_token_command = get_join_token(role="worker")
            print(f"Join token for manager is {manager_join_token_command}")
            print(f"Join token for worker is {worker_join_token_command}")
            swarm.join()
            if restart_swarm:
                self.machines = build_machines(["web"])#["node", "task", "web", "haproxy", "push"])
            else:
                self.machines = machine.ls()

            for m in self.machines:

                print(f"machine {m['Name']} built")
                # TODO
                machine_ips = [(x['Name'], x.get("URL")) for x in machine.ls()]
                print(machine_ips)
                import pdb; pdb.set_trace()

                # create managers and workers for every manifest
                # get IPs of manager nodes, use for rendering haproxy
                # use join token to join docker swarm
                #docker.service.create()

def deploy():
    try:
        name = "newsblur_dev"
        docker_swarm = DockerCluster(name, restart_swarm=True)
        for machine in docker_swarm.machines:
            if f"{machine['Name']}.yml" not in os.listdir('machine_compose'):
                print(f"{machine['Name']}.yml not found")
            else:
                build_containers(machine['Name'])
    except Exception as e:
        print(e)
