#coding:utf-8
#!/usr/bin/python3
"""ctf web scan
Author: D4rk
TODO: 针对某些全站200的情况，分析返回数据包匹配"404 not found 未找到页面"字样
"""

import sys
import requests

class bcolors:
    """terminal colors"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    SKY = '\033[36m'
    WHITE = '\033[37m'
    ENDC = '\033[0m'

def dir_scan(url):
    """scan directories"""
    with open('dir.txt') as f:
        lines = f.read().splitlines()
    f.close()

    for line in lines:
        r = requests.get(url+line)
        if r.status_code == 200:
            print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
            file_scan(url+line)

def file_scan(url):
    """scan files"""
    with open('dic.txt') as f:
        lines = f.read().splitlines()
    f.close()

    for line in lines:
        r = requests.get(url+line)
        if r.status_code == 200:
            print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
            check_source_leak(url, line)

def check_source_leak(url, filename):
    """print source leak results"""
    leak1 = '.' + filename + '.swp'
    leak2 = '.' + filename + '.swo'
    leak3 = filename + '.bak'
    leak4 = filename + '~'
    leaks = [leak1, leak2, leak3, leak4]
    for leak in leaks:
        r = requests.get(url+leak)
        if r.status_code == 200:
            print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + leak)

def main():
    """main function"""
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f1:
            webs = f1.read().splitlines()
        f1.close()
        for web in webs:
            file_scan(web)
            dir_scan(web)
    else:
        print("Usage: python main.py xxx.txt")

if __name__ == '__main__':
    main()
