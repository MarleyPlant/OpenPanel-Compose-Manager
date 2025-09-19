# docker.py

"""
OpenPanel Docker Module Entry Point.

This module serves as the main entry point for the OpenPanel Docker management
module. It handles the registration of Flask blueprints and sets up the necessary
routing for Docker Compose management functionality.

Note:
    The .py file needs to have the same name as the folder for proper OpenPanel
    module discovery and import functionality.

Example:
    If the folder is 'docker', the file needs to be named 'docker.py' to be
    imported correctly by OpenPanel.
"""

# import what is needed for this plugin
import os
import sys
from flask import render_template_string
from app import (
    app,
    login_required_route,
    get_user_services_and_domains,
    inject_data,
)
from flask_babel import Babel, _

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# STEP 1: Import all route modules FIRST to ensure all @blueprint.route decorators execute
print("Loading route modules...")
import routes.index  # This must load all routes and create the blueprint
import routes.stack

# STEP 2: Import the blueprint AFTER routes are loaded
print("Importing blueprint...")
from routes.index import composerdashboard
from routes.stack import composerstack


# STEP 4: Register the blueprint with the Flask app
print("Registering blueprint with app...")
app.register_blueprint(composerdashboard)
app.register_blueprint(composerstack)

# STEP 6: Debug - Print registered blueprints
print("=== REGISTERED BLUEPRINTS ===")
for name, blueprint in app.blueprints.items():
    if "compose" in name or "docker" in name or "ptk" in name:
        print(f"  {name}: {blueprint.url_prefix}")

print("Docker module loaded successfully with blueprint registration.")
