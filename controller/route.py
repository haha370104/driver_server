from flask import Blueprint, request, make_response, session, redirect, url_for
from global_var import route
import json

route_bp = Blueprint('route', __name__)


@route_bp.route('/check_login/')
def check_login():
    if route.check_login():
        return json.dumps({'msg': '已经登录'})
    else:
        route.login()
        return check_login()


@route_bp.route('/get_device_id/')
def get_device_id():
    return json.dumps(route.get_device_id())


@route_bp.route('/add_task/', methods=['GET', 'POST'])
def add_task():
    url = request.values.get('url')
    device_id = request.values.get('device_id')
    return route.download(device_id, url)
