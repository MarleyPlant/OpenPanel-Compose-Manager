"""
Stack Model for OpenPanel Docker Module.

This module defines the Stack class which represents a Docker Compose stack
configuration including services, environment variables, and deployment settings.
"""

import os
from flask_babel import Babel, _

import yaml
from models.service import Service
import ptkutils

from models.dockercompose import DockerCompose


class Stack:
    """
    Represents a Docker Compose stack with configuration and services.

    A Stack encapsulates a Docker Compose configuration along with OpenPanel-specific
    metadata such as UI labels, descriptions, and deployment commands.

    Attributes:
        path (str): Filesystem path to the stack directory.
        compose (DockerCompose): Docker Compose configuration object.
        stackconfig (dict): Stack configuration from stack.yml.
        _services (list): List of services in the stack.
        envfiles (dict): Environment file configurations.

    Example:
        >>> stack = Stack("/path/to/stack/directory")
        >>> print(stack.data['name'])
        >>> for service in stack.services:
        ...     print(service['name'])
    """

    def __init__(self, path):
        """
        Initialize a new Stack instance.

        Args:
            path (str): Path to the directory containing stack.yml and related files.

        Note:
            The stack configuration is automatically loaded during initialization.
        """
        self.path = path
        self.compose = None
        self.stackconfig = None
        self._services = []
        self.envfiles = {}
        self.load_stack()

    @property
    def services(self):
        """
        Get the list of services in this stack.

        Returns:
            list: List of service data dictionaries.
        """
        result = []
        for service in self._services:
            result.append(service.data)
        return result
    
    
    @property
    def volumes(self):
        """
        Get all volume mappings from all services in the stack.

        Returns:
            dict: Combined volume mappings from all services.
        """
        volumes = {}
        for service in self._services:
            if service.volumes:
                for volume in service.volumes:
                    volumes[volume['container']] = {"container": volume['container'], "host": volume['host'], "service": service.key}

        return volumes

    @property
    def ports(self):
        """
        Get all port mappings from all services in the stack.

        Returns:
            dict: Combined port mappings from all services.
        """
        ports = {}
        for service in self._services:
            if service.ports:
                for key, value in service.ports.items():
                    ports[key] = value
        return ports

    @property
    def env(self):
        """
        Get all environment variables from all services in the stack.

        Returns:
            dict: Combined environment variables from all services.
        """
        variables = {}
        for service in self._services:
            print("Getting env for service:", service.key)
            print("Service env:", service.env)
            if service.env:
                for key in service.env:
                    variables[key] = service.env[key]
        return variables

    @property
    def data(self):
        """
        Get the complete stack data as a dictionary.

        Returns:
            dict: Complete stack configuration including metadata, services,
                 ports, environment variables, and compose file content.
        """
        return {
            "name": self.stackconfig.get("name", os.path.basename(self.path).lower()),
            "label": self.stackconfig.get(
                "label", os.path.basename(self.path).replace("_", " ").title()
            ),
            "icon": self.stackconfig.get("icon", "fa fa-cubes"),
            "services": self.services,
            "volumes": self.volumes,
            "ports": self.ports,
            "description": _(self.stackconfig.get("description", "")),
            "commands": self.stackconfig.get("commands", []),
            "compose_file": yaml.dump(self.compose.data),
            "env": self.env,
        }

    def updateCompose(self):
        """
        Update the Docker Compose configuration with current service data.

        This method synchronizes the internal service configurations with
        the underlying Docker Compose object.
        """
        for service in self._services:
            self.compose.services[service.key] = service

    def load_services(self):
        """
        Load services from the stack configuration.

        Reads the 'containers' section from stack.yml and loads the corresponding
        service configurations from the Docker Compose file.
        """
        services = self.stackconfig.get("containers", [])
        if not services:
            print("No services defined in stack.yml")
            return
        else:
            container_prefix = self.stackconfig.get("container_prefix", False)

            for service in services:
                if container_prefix:
                    service = self.compose.findServiceByName(
                        container_prefix + "-" + service
                    )
                if type(service) is not Service:
                    service = self.compose.findServiceByName(service)

                if type(service) is not Service:
                    print("Service not found in root docker-compose.yml:", service)
                    continue

                self._services.append(service)

    def load_stack(self):
        """
        Load the stack configuration from the filesystem.

        Reads stack.yml from the stack directory and initializes the
        Docker Compose configuration and services.
        """
        stack_file = os.path.join(self.path, "stack.yml")
        self.compose = DockerCompose("/home/yolo")

        if os.path.exists(stack_file):
            self.stackconfig = ptkutils.load_yaml_string(
                ptkutils.getFileContents(stack_file)
            )
            self.load_services()

        else:
            print("stack.yml not found in", self.path)
            return
