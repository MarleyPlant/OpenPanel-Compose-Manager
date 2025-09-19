
import os

from models.env import ENVFile



class Service:
    def __init__(self, config, key):
        self.config = config
        self.env = {}
        self.ports = {}
        self.volumes = []
        self.key = key
        self.envfile = None
        self.loadEnv()
        self.loadPorts()
        self.loadVolumes()
        print(f"Initialized service: {self.key}")
        print(f"Service env: {self.env}")

    @property
    def data(self):
        data = self.config
        data["environment"] = self.env
        data["ports"] = self.ports
        data["volumes"] = self.volumes
        return data

    @property
    def compose(self):
        data = self.config
        data["environment"] = self.env
        data["ports"] = self.ports
        data["volumes"] = self.volumes
        return data
    
    def loadVolumes(self):
        for volume in self.config.get("volumes", []):
            if isinstance(volume, str):
                host_volume, container_volume = volume.split(":", 1)
                self.volumes.append({"host": host_volume, "container": container_volume})

    def loadPorts(self):
        for port in self.config.get("ports", []):
            if isinstance(port, str):
                if ":" in port:
                    host_port, container_port = port.split(":", 1)
                    self.ports[container_port] = host_port

    def loadEnv(self):
        if "env_file" in self.config:
            if isinstance(self.config["env_file"], str):
                envfile = ENVFile(os.path(self.config["env_file"]))
                self.envfile = envfile

        if "environment" in self.config:
            print("Loading environment for service:", self.key)
            for env in self.config["environment"]:
                print("Processing env:", env)
                if isinstance(env, str):
                    if "=" in env:
                        key, value = env.split("=", 1)
                        self.env[key] = value
                elif isinstance(env, dict):
                    for key, value in env.items():
                        self.env[key] = value
                        
            