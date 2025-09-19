import os

from models.service import Service
import yaml
import ptkutils

class DockerCompose:
    def __init__(self, path):
        self.path = path
        self.compose = None
        self.services = {}
        self.load_compose()

    @property
    def data(self):
        for service in self.services:
            self.compose["services"][self.services[service].key] = self.services[
                service
            ].data
        return self.compose


    def load_compose(self):
        compose_file = os.path.join(self.path, "docker-compose.yml")

        if os.path.exists(compose_file):
            print("Loading docker-compose.yml from", compose_file)
            self.compose = ptkutils.load_yaml_file(compose_file)
            services = self.compose.get("services", [])
            if not services:
                print("No services defined in docker-compose.yml")
                return
            else:
                for service in services:
                    self.services[service] = Service(services[service], service)

    def findServiceByName(self, name):
        print("Finding service by name:")
        if name in self.services:
            return self.services[name]
        else:
            for service in self.services:
                if self.services[service].config.get("container_name", "") == name:
                    return self.services[service]
        return None