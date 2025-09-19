"""
Data Management for OpenPanel Docker Module.

This module handles the loading and management of Docker Compose stacks from
the data directory. It provides functions to discover, load, and retrieve
stack configurations.
"""

from flask_babel import Babel, _
import os
from models.stack import Stack
import yaml


# Global list to store all discovered Docker Compose stacks
stacks = []

# Automatically discover and load all stacks from the data directory
data_path = os.path.join(os.path.dirname(__file__), "data")
for folder in os.listdir(data_path):
    folder_path = os.path.join(data_path, folder)
    if os.path.isdir(folder_path):
        stack = Stack(folder_path)
        if stack:
            stacks.append(stack.data)


def getStackByName(name):
    """
    Retrieve a stack configuration by its name.
    
    Args:
        name (str): The name of the stack to retrieve.
        
    Returns:
        dict or None: Stack configuration dictionary if found, None otherwise.
        
    Example:
        >>> stack = getStackByName("wordpress")
        >>> if stack:
        ...     print(f"Found stack: {stack['name']}")
        >>> else:
        ...     print("Stack not found")
    """
    for stack in stacks:
        if stack["name"] == name:
            return stack
    return None
