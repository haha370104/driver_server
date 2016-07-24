from global_var import torrent
from flask import Blueprint, request
import json

torrent_bp = Blueprint('torrent', __name__)


@torrent_bp.route('/search/<string:keyword>/')
def search(keyword):
    return json.dumps(torrent.get_detail_lists(keyword))


@torrent_bp.route('/get_download_url/')
def get_download_url():
    url = request.values.get('url')
    return json.dumps(torrent.get_download_url(url))