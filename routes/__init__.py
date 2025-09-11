from flask import Blueprint, render_template_string, request
from flask_babel import _
from app import inject_data, get_user_services_and_domains, login_required_route
import app as openpanel
import os

compose_manager_bp = Blueprint('compose_manager', __name__)

@compose_manager_bp.route('/advanced/composemanager/stack/<stack_name>/', methods=['GET', 'POST'])
@login_required_route
def traceroute(stack_name):
    current_username = inject_data().get('user_id')
    user_services_and_domains = get_user_services_and_domains(current_username)
    # If POST request, handle form submission here and redirect user
    if request.method == 'POST':
        args = (subdirectory, domain, service_name)
        if app_port is not None:
            args += (app_port,)
        # result = config_func(*args)
        return '', 204, {'HX-Redirect': '../..'}
    template_path = os.path.join(os.path.dirname(__file__), 'templates/editstack.html')
    with open(template_path) as f:
        template = f.read()
    return render_template_string(
        template,
        app=dir(openpanel),
        stack_name=stack_name,
        services=[{'name': 'traceroute', 'label': _('Traceroute'), 'icon': 'fa-solid fa-route'}],
        domains=user_services_and_domains[1],
        title=_('Edit Stack {stack_name}'),
    )
