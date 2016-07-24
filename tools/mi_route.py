import requests
import hashlib
import time
import json
import base64
from pyquery import PyQuery as pq


def md5(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest().upper()


class mi_route():
    phone_num = ''
    pwd = ''
    __session = None
    __serviceToken = ''
    __xiaoqiang_d2r_ph = ''

    def __init__(self, phone, pwd):
        self.__session = requests.session()
        self.phone_num = phone
        self.pwd = md5(pwd)
        self.userId = ''

    def check_login(self):
        response_text = self.__session.get('https://d.miwifi.com/d2r').text
        if '登录小米账号' in response_text:
            return False
        else:
            return True

    def login(self):
        para = {'_json': 'true',
                'callback': 'https://d.miwifi.com/sts?followup=https%3A%2F%2Fd.miwifi.com%2Fd2r%2F&sign=x1QKHaEj4k5EcPUB1DXJi8dXvzY%3D',
                'sid': 'xiaoqiang_d2r',
                'qs': '%3Fmini%3Dfalse%26callback%3Dhttps%253A%252F%252Fd.miwifi.com%252Fsts%253Ffollowup%253Dhttps%25253A%25252F%25252Fd.miwifi.com%25252Fd2r%25252F%2526sign%253Dx1QKHaEj4k5EcPUB1DXJi8dXvzY%25253D%26sid%3Dxiaoqiang_d2r',
                '_sign': '1t2ptn1BcJ9v7DIuhHfqmL4YvBY=',
                'serviceParam': '{"checkSafePhone":false}',
                'user': self.phone_num,
                'hash': self.pwd}
        dc = int(time.time() * 1000)
        url = 'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc={0}'.format(str(dc))
        r = self.__session.post(url, para)
        response_data = r.text.lstrip('&').lstrip('START').lstrip('&')
        if '失败' in response_data:
            return False
        response_data = json.loads(response_data)
        self.userId = r.cookies.get('userId', domain='.xiaomi.com')
        url = response_data['location']
        self.__session.get(url)
        self.__serviceToken = self.__session.cookies['serviceToken']
        self.__xiaoqiang_d2r_ph = self.__session.cookies['xiaoqiang_d2r_ph']
        return True

    def get_device_id(self):
        url = 'https://d.miwifi.com/d2r'
        params = {
            'userId': self.userId
        }
        response_HTML = self.__session.get(url, params=params).text
        HTML = pq(response_HTML)
        devices = HTML('div.device-grid.device-image-r1cm')
        devices_id = []
        for d in devices:
            id = devices(d).attr('data-device-id')
            name = devices(d).attr('title')
            devices_id.append({'device_id': id, 'device_name': name})
        return devices_id

    def download(self, device_id, url):
        url_encode = base64.b64encode(url.encode())
        download_para = {'userId': self.userId,
                         'xiaoqiang_d2r_ph': self.__xiaoqiang_d2r_ph,
                         'serviceToken': self.__serviceToken,
                         'src': '',
                         'deviceId': device_id,
                         'url': url_encode}
        r = self.__session.post('https://d.miwifi.com/d2r/download2RouterApi', download_para)
        result = json.loads(r.text)
        if result.get('R') == 401:
            if self.login():
                result = self.download(device_id, url)
        return result
