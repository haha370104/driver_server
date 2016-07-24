import requests
import re
from pyquery import PyQuery as pq


class torrentkitty:
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    def get_detail_lists(self, keyword):
        base_url = 'https://www.torrentkitty.tv'
        response = requests.get(base_url + '/search/{0}/'.format(keyword), headers=self.headers)
        response.encoding = 'UTF-8'
        HTML = pq(response.text)
        results = HTML('table#archiveResult tr')
        download_lists = []
        for i in range(len(results)):
            if i == 0:
                continue
            file_name = results.eq(i)('td.name').text()
            detail_url = results.eq(i)('td.action').children().eq(0).attr('href')
            download_lists.append({'name': file_name, 'detail_url': detail_url})
        return download_lists

    def get_download_url(self, detail_url):
        base_url = 'https://www.torrentkitty.tv'
        response = requests.get(base_url + detail_url, headers=self.headers)
        detail_HTML = pq(response.text)
        download_url = detail_HTML('textarea.magnet-link').eq(0).text()
        file_size = detail_HTML('table.detailSummary tr td').eq(3).text()
        result = {'size': file_size, 'url': download_url}
        return result


if __name__ == '__main__':
    test = torrentkitty()
    print(test.get_download_url(test.get_detail_lists('魔兽')[0]['detail_url']))
