# traceroute.py

'''
.py file needs to have the same name as the folder, so f folder is 'traceoute' file needs to be named 'traceroute.py' in order to be imported.
'''

# import flask app
from flask import Flask, render_template, render_template_string, request

# import what is needed for this plugin
import socket
import struct
import time
import os
import requests
import inspect

# For translations
# https://python-babel.github.io/flask-babel/
from flask_babel import Babel, _

# Import stuff from OpenPanel core
from app import app, get_user_services_and_domains, inject_data, get_openpanel_ip, login_required_route
import app as openpanel  # This lets you access all attributes and functions in the app module

# from modules.docker import get_env_value
# from modules.pm2 import edit_apache_config, edit_nginx_config, edit_lsws_config

# web_server_type = get_env_value('WEB_SERVER')

# server_map = {
#     "apache": ("Apache", edit_apache_config),
#     "nginx": ("Nginx", edit_nginx_config),
#     "openresty": ("OpenResty", edit_nginx_config),
#     "openlitespeed": ("OpenLitespeed", edit_lsws_config),
#     "litespeed": ("Litespeed", edit_lsws_config),
# }

# server_name, config_func = server_map.get(web_server_type, (None, None))


# custom funtion example
def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        client_ip = request.remote_addr

    return client_ip



# Route should be same as 'link' in readme.txt
@app.route('/advanced/composemanager/', methods=['GET', 'POST'])
# remove login_required_route decorator if page should be accessed without login (NOT RECOMMENDED)
@login_required_route
def compose_manager():

    # this is needed for tempaltes to overwrite global templates folder
    #exit the html file name accordingly
    template_path = os.path.join(os.path.dirname(__file__), 'templates/traceroute.html')
    with open(template_path) as f:
        template = f.read()
   

    return render_template_string(
        template,
        title=_('Traceroute'), # title is shown in breadcrumbs and browser tab
        stacks=[{'name': 'traceroute', 'label': _('Traceroute'), 'icon': 'fa-solid fa-route'}], # icon is from https://fontawesome.com/icons/route?s=solid
    )
    

# Route should be same as 'link' in readme.txt
@app.route('/advanced/composemanager/stack/<stack_name>/', methods=['GET', 'POST'])
# remove login_required_route decorator if page should be accessed without login (NOT RECOMMENDED)
@login_required_route
def traceroute(stack_name):
    current_username = inject_data().get('user_id') # returns username of the current openpanel account
    user_services_and_domains = get_user_services_and_domains(current_username)
       
       
       
       # If POST request, handle form submission here and redirect user
    if request.method == 'POST':
        
        # redirect user after form submission
        return '', 204, {'HX-Redirect': '../..'}  # redirect to composemanager main page
               
    # this is needed for tempaltes to overwrite global templates folder
    #exit the html file name accordingly
    template_path = os.path.join(os.path.dirname(__file__), 'templates/editstack.html')
    with open(template_path) as f:
        template = f.read()

    return render_template_string(
        template,
        app=dir(openpanel),
        stack_name=stack_name,
        ports=[
            230, 2323, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009,
        ],
        services=[
            {'name': 'traceroute', 'label': _('Traceroute'), 'icon': 'fa-solid fa-route'}
        ],
        domains=user_services_and_domains[1],
        title=_('Edit Stack {stack_name}'), # title is shown in breadcrumbs and browser tab
    )

