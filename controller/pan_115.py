from flask import Blueprint, redirect, url_for, render_template, request
from global_var import pan
import json
import threading

pan_bp = Blueprint('pan', __name__)


@pan_bp.route('/check_login/')
def check_login():
    if pan.check_login():
        return json.dumps({'msg': '已经登录', 'status': True})
    else:
        return json.dumps({'msg': '尚未登录/登录失败', 'status': False})


@pan_bp.route('/get_code/')
def get_code():
    pan.get_code(path='static/image/')
    return render_template('code.html')


@pan_bp.route('/wait_login/')
def wait_login():
    if pan.wait_login():
        pan.login()
        threading.Thread(target=pan.keep_login)
        return redirect(url_for('pan.check_login'))
    else:
        return json.dumps({'msg': '登录超时', 'status': False})


@pan_bp.route('/add_task/', methods=['GET', 'POST'])
def add_task():
    url = request.values.get('url')
    return json.dumps(pan.add_task(url))


@pan_bp.route('/get_task_list/', methods=['GET', 'POST'])
def get_task_list():
    page = request.values.get('page')
    if page == None:
        page = 1
    return json.dumps(pan.get_task_list(page))


@pan_bp.route('/get_files/<string:cid>/<int:page>/<int:type>/', methods=['GET', 'POST'])
def get_files(cid, page, type):
    return json.dumps(pan.get_files_by_cid(cid, type, page))  # 4是视频


@pan_bp.route('/get_download_url/', methods=['GET', 'POST'])
def get_download_url():
    pick_code = request.values.get('pick_code')
    return json.dumps(pan.get_download_url(pick_code))
