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
composerstack = Blueprint(
    "ptkcomposerstack", __name__, url_prefix="/containers/compose/stack", template_folder=os.path.join(os.path.dirname(__file__), "../templates")
)


@composerstack.route("/<stack_name>/", methods=["GET", "POST"])
def stack_detail(stack_name):
    """
    Display details for a specific Docker Compose stack.
    
    Args:
        stack_name (str): Name of the stack to display
        
    Returns:
        str: Rendered HTML template for stack details
    """
    print(f"stack_detail route called for: {stack_name}")
    
    try:
        # Manual authentication check - bypass the decorator
        user_data = inject_data()
        if not user_data or not user_data.get("current_username"):
            # Redirect to login if not authenticated
            return f'<script>window.location.href="/login";</script>', 403
        
        current_username = user_data.get("current_username")
        user_id = user_data.get("user_id")
        user_services_and_domains = get_user_services_and_domains(current_username)
        
        stack = ptkdata.getStackByName(stack_name)
        if not stack:
            return "Stack not found", 404
        
        template = ptkutils.openTemplate("stack/[name]/index.html")
        if not template:
            return "Template not found: stack/[name]/index.html", 500
            
        return render_template_string(
            template,
            title=_(stack['label']),
            stack=stack,
            domains=user_services_and_domains[1] if user_services_and_domains else [],
            user_id=user_id,
            current_username=current_username
        )
    except Exception as e:
        return f"Error in stack_detail: {str(e)}", 500


@composerstack.route("/<stack_name>/services/", methods=["GET"])
def stack_services(stack_name):
    """
    Display services for a specific stack.
    
    Args:
        stack_name (str): Name of the stack
        
    Returns:
        str: Rendered HTML template for stack services
    """
    print(f"stack_services route called for: {stack_name}")
    
    try:
        # Manual authentication check - bypass the decorator
        user_data = inject_data()
        if not user_data or not user_data.get("current_username"):
            # Redirect to login if not authenticated
            return f'<script>window.location.href="/login";</script>', 403
        
        current_username = user_data.get("current_username")
        user_id = user_data.get("user_id")
        user_services_and_domains = get_user_services_and_domains(current_username)
        
        stack = ptkdata.getStackByName(stack_name)
        if not stack:
            return "Stack not found", 404
            
        template = ptkutils.openTemplate("stack/[name]/services.html")
        if not template:
            return "Template not found: stack/[name]/services.html", 500
            
        return render_template_string(
            template,
            title=_(f"Services: {stack['label']}"),
            stack=stack,
            services=stack.get('services', []),
            domains=user_services_and_domains[1] if user_services_and_domains else [],
            user_id=user_id,
            current_username=current_username
        )
    except Exception as e:
        return f"Error in stack_services: {str(e)}", 500


@composerstack.route("/<stack_name>/edit/", methods=["GET", "POST"])
def stack_edit(stack_name):
    """
    Edit a specific Docker Compose stack.
    
    Args:
        stack_name (str): Name of the stack to edit
        
    Returns:
        str: Rendered HTML template for stack editing
    """
    print(f"stack_edit route called for: {stack_name}")
    
    try:
        # Manual authentication check - bypass the decorator
        user_data = inject_data()
        if not user_data or not user_data.get("current_username"):
            # Redirect to login if not authenticated
            return f'<script>window.location.href="/login";</script>', 403
        
        current_username = user_data.get("current_username")
        user_id = user_data.get("user_id")
        user_services_and_domains = get_user_services_and_domains(current_username)
        
        stack = ptkdata.getStackByName(stack_name)
        if not stack:
            return "Stack not found", 404
        
        # Handle POST request for form submission
        if request.method == "POST":
            # Process form data here
            # For now, redirect back to stack detail page
            return f'<script>window.location.href="{url_for("ptkcomposemanager.stack_detail", stack_name=stack_name)}";</script>'
        
        template = ptkutils.openTemplate("stack/[name]/edit.html")
        if not template:
            return "Template not found: stack/[name]/edit.html", 500
            
        return render_template_string(
            template,
            title=stack['label'],
            stack=stack,
            domains=user_services_and_domains[1] if user_services_and_domains else [],
            user_id=user_id,
            current_username=current_username
        )
    except Exception as e:
        return f"Error in stack_edit: {str(e)}", 500