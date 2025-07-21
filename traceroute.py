# traceroute.py

'''
.py file needs to have the same name as the folder, so f folder is 'traceoute' file needs to be named 'traceroute.py' in order to be imported.
'''

# import flask app
from flask import Flask, render_template, render_template_string, request

# import what is needed for this plugin
import subprocess
import os
import requests

# For translations
# https://python-babel.github.io/flask-babel/
from flask_babel import Babel, _

# Import stuff from OpenPanel core
from app import app, inject_data, get_openpanel_ip, login_required_route

# custom funtion example
def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        client_ip = request.remote_addr

    return client_ip

# Route should be same as 'link' in readme.txt
@app.route('/advanced/traceroute', methods=['GET', 'POST'])
# remove login_required_route decorator if page should be accessed without login (NOT RECOMMENDED)
@login_required_route
def traceroute():
    result = ""
    if request.method == 'POST':
        target = request.form.get('target')
        if target:
            try:
                process = subprocess.run(
                    ['traceroute', '-n', target],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=30
                )
                result = process.stdout
            except Exception as e:
                result = f"Error: {str(e)}"
        else:
            # use _( ) to allow localization of the text
            result = _("Please enter a valid IP address or hostname.")

    # this is needed for tempaltes to overwrite global templates folder
    #exit the html file name accordingly
    template_path = os.path.join(os.path.dirname(__file__), 'traceroute.html')
    with open(template_path) as f:
        template = f.read()

    # return ip address for openpanel account
    current_username = inject_data().get('current_username') # returns username of the current openpanel account
    server_ip = get_openpanel_ip(current_username) # returns IP for the current openpanel account
    client_ip = get_client_ip() # returns ip form our cusotm function

    return render_template_string(
        template,
        title=_('Traceroute'), # title is shown in breadcrumbs and browser tab
        server_ip=server_ip,
        client_ip=client_ip,
        result=result
    )
