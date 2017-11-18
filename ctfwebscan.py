#coding: utf-8
#author: D4rk

'''
ctf web scan
'''

import sys
import urllib.request
import urllib.parse

def scan(url):
    '''scan function'''
    # 读取dic.txt中的内容存进lines
    with open('dic.txt') as f2:
        lines = f2.read().splitlines()
    f2.close()
    # logs列表用于存储有效请求记录
    logs = []
    for line in lines:
        try:
            # 设置data
            #values = {}
            #data = urllib.parse.urlencode(values)
            # 设置headers
            #user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0"
            #headers = {'User-Agent': user_agent}
            # 发送请求
            #request = urllib.request.Request(url+line, data, headers)
            #response = urllib.request.urlopen(request)
            response = urllib.request.urlopen(url+line)
            info = '[+] '+url+line
            if response.code == 200:
                print(info)
                logs.append(info)
        except urllib.request.HTTPError:
            pass
    '''
    for log in logs:
        print log
    '''

if __name__ == '__main__':
    if len(sys.argv) == 2:
        # 读取xxxctf-2017.txt中的内容存进webs
        with open(sys.argv[1]) as f1:
            webs = f1.read().splitlines()
        f1.close()
        for web in webs:
            scan(web)
    else:
        print("Usage: python ctfwebscan.py xxxctf-2017.txt")
