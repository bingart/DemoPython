import sys
import requests

from stem.control import Controller

if __name__ == '__main__':
    proxies = {
        'http': 'socks5://127.0.0.1:9350',
        'https': 'socks5://127.0.0.1:9350'
    }
    resp = requests.get('https://www.infosoap.com/ip.php', proxies=proxies)
    if resp.status_code == 200:
        html = resp.content.decode('utf-8')
        print ('html={0}'.format(html))
