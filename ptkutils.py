"""
Utility Functions for OpenPanel Docker Module.

This module provides utility functions for YAML processing, file operations,
and Flask blueprint management for the Docker Compose management functionality.
"""

import yaml
import os


def load_yaml_string(yaml_string):
    """
    Load and parse a YAML string into a Python object.
    
    Args:
        yaml_string (str): The YAML content as a string.
        
    Returns:
        dict or None: Parsed YAML data as a Python object, or None if parsing fails.
        
    Example:
        >>> yaml_content = "name: test\nversion: 1.0"
        >>> data = load_yaml_string(yaml_content)
        >>> print(data['name'])
        test
    """
    try:
        return yaml.safe_load(yaml_string)
    except yaml.YAMLError as e:
        print(f"Error loading YAML: {e}")
        return None
    
def load_yaml_file(file_path):
    """
    Load and parse a YAML file into a Python object.
    
    Args:
        file_path (str): Path to the YAML file relative to the data directory.
        
    Returns:
        dict or None: Parsed YAML data, or None if loading fails.
        
    Example:
        >>> data = load_yaml_file("mystack/stack.yml")
        >>> print(data['name'])
    """
    contents = getFileContents(file_path)
    return load_yaml_string(contents)

def getServices(stack):
    """
    Extract services configuration from a Docker Compose stack.
    
    Args:
        stack (dict): Docker Compose stack configuration.
        
    Returns:
        list: List of services in the stack, empty list if no services found.
        
    Example:
        >>> stack = {"services": ["web", "db"]}
        >>> services = getServices(stack)
        >>> print(services)
        ['web', 'db']
    """
    return stack.get("services", [])

def getFileContents(filename):
    """
    Read the contents of a file from the data directory.
    
    Args:
        filename (str): Name of the file to read from the data directory.
        
    Returns:
        str: Contents of the file.
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
        IOError: If there's an error reading the file.
        
    Example:
        >>> content = getFileContents("mystack/docker-compose.yml")
        >>> print(len(content))
    """
    template_path = os.path.join(os.path.dirname(__file__), "data/")

    with open(os.path.join(template_path, filename), "r") as f:
        return f.read()
    
def openTemplate(path):
    """
    Load a template file from the templates directory.
    
    Args:
        path (str): Path to the template file relative to the templates directory.
        
    Returns:
        str: Contents of the template file, empty string if file not found.
        
    Example:
        >>> template = openTemplate("index.html")
        >>> if template:
        ...     print("Template loaded successfully")
    """
    template_path = os.path.join(os.path.dirname(__file__), "templates", path)
    if not os.path.exists(template_path):
        print("Template file not found:", template_path)
        return ""
    
    with open(template_path) as f:
        template = f.read()
    
    return template

# Configuration constants
rootpath = "/containers/compose/"

# Flask blueprint for Docker Compose management routes

