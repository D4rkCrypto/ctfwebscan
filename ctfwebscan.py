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

    for line in lines:
        try:
            response = urllib.request.urlopen(url+line)
            if response.code == 200:
                print('[+] '+url+line)
                check_source_leak(url, line)
        except urllib.request.HTTPError:
            pass

def check_source_leak(url, filename):
    leak1 = '.' + filename + '.swp'
    leak2 = '.' + filename + '.swo'
    leak3 = filename + '.bak'
    leak4 = filename + '~'
    leaks = [leak1, leak2, leak3, leak4]
    for leak in leaks:
        try:
            response = urllib.request.urlopen(url+leak)
            if response.code == 200:
                print('[+] '+url+leak)
        except urllib.request.HTTPError:
            pass

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
