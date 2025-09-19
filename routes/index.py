"""
Main Routes for OpenPanel Docker Module.

This module defines the primary Flask routes for the Docker Compose management
interface using Flask blueprints.
"""

import os
import ptkdata
import ptkutils

from flask import Blueprint, render_template, render_template_string, request, jsonify, url_for
from flask_babel import Babel, _

# Import stuff from OpenPanel core
from app import (
    login_required_route,
    get_user_services_and_domains,
    inject_data,
)
# Create the blueprint FIRST
composerdashboard = Blueprint(
    "ptkcomposemanager", __name__, url_prefix="/containers/compose", template_folder=os.path.join(os.path.dirname(__file__), "../templates")
)

# Debug: Print blueprint creation
print(f"Created blueprint: {composerdashboard.name} with prefix: {composerdashboard.url_prefix}")


# THEN define all routes on the blueprint
@composerdashboard.route("/", methods=["GET", "POST"])
def compose_manager():
    """
    Main Docker Compose management dashboard.

    Displays the list of available Docker Compose stacks and provides
    the main interface for stack management operations.

    Returns:
        str: Rendered HTML template for the compose manager dashboard.

    Note:
        This route includes manual authentication check instead of using
        the problematic login_required_route decorator with blueprints.
    """
    print("compose_manager route called!")  # Debug output
    
    try:
        # Manual authentication check - bypass the decorator
        user_data = inject_data()
        if not user_data or not user_data.get("current_username"):
            # Redirect to login if not authenticated
            return f'<script>window.location.href="/login";</script>', 403
        
        current_username = user_data.get("current_username")
        user_id = user_data.get("user_id")
        user_services_and_domains = get_user_services_and_domains(current_username)
        
        template = ptkutils.openTemplate("index.html")
        if not template:
            return "Template not found: index.html", 500

        return render_template_string(
            template,
            title=_("Compose Manager"),
            stacks=ptkdata.stacks,
            domains=user_services_and_domains[1] if user_services_and_domains else [],
            user_id=user_id,
            current_username=current_username
        )
    except Exception as e:
        return f"Error in compose_manager: {str(e)}", 500



# Debug: Print that all routes are defined (Blueprint routes aren't accessible until registered)
print(f"Blueprint {composerdashboard.name} routes defined successfully")
print("Routes will be available after blueprint registration with Flask app")


# Test route without authentication for debugging
@composerdashboard.route("/test", methods=["GET"])
def test_route():
    """Test route to verify blueprint registration works."""
    return f"<h1>Blueprint Test Successful!</h1><p>Blueprint '{composerdashboard.name}' is working correctly!</p><p>URL prefix: {composerdashboard.url_prefix}</p>"


# Diagnostic route to test authentication functions
@composerdashboard.route("/debug", methods=["GET"])
def debug_auth():
    """Debug route to test authentication functions."""
    try:
        # Test if inject_data works
        user_data = inject_data()
        current_username = user_data.get("current_username")  # FIXED: Use 'current_username'
        user_id = user_data.get("user_id")
        
        # Test if get_user_services_and_domains works
        if current_username:
            user_services_and_domains = get_user_services_and_domains(current_username)
            domains = user_services_and_domains[1] if user_services_and_domains else []
        else:
            domains = []
            
        return f"""
        <h1>Authentication Debug - FIXED</h1>
        <p><strong>User Data:</strong> {user_data}</p>
        <p><strong>User ID:</strong> {user_id}</p>
        <p><strong>Current Username (FIXED):</strong> {current_username}</p>
        <p><strong>Domains:</strong> {domains}</p>
        <p><strong>inject_data() works:</strong> {'✓' if user_data else '✗'}</p>
        <p><strong>User logged in:</strong> {'✓' if current_username else '✗'}</p>
        <hr>
        <p><strong>Fix Applied:</strong> Now using 'current_username' instead of 'user_id'</p>
        <p><strong>Test Links:</strong></p>
        <ul>
            <li><a href="/containers/compose/">Main Dashboard</a> (should work now)</li>
            <li><a href="/containers/compose/stack/kimai/">Kimai Stack</a> (should work now)</li>
        </ul>
        """
    except Exception as e:
        return f"""
        <h1>Authentication Debug - ERROR</h1>
        <p><strong>Error:</strong> {str(e)}</p>
        <p><strong>Error Type:</strong> {type(e).__name__}</p>
        <hr>
        <p>This indicates an issue with the authentication functions.</p>
        """
