#!/usr/bin/python3
"""ctf web scan
Author: D4rk
TODO: 针对某些全站200的情况，分析返回数据包匹配"404 not found 未找到页面"字样
"""

import sys
import urllib.request
import urllib.parse

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
        try:
            response = urllib.request.urlopen(url+line)
            if response.code == 200:
                print(bcolors.GREEN + str(response.code) + ' ' + bcolors.ENDC + url + line)
                file_scan(url+line)
        except urllib.request.HTTPError:
            pass

def file_scan(url):
    """scan files"""
    with open('dic.txt') as f:
        lines = f.read().splitlines()
    f.close()

    for line in lines:
        try:
            response = urllib.request.urlopen(url+line)
            if response.code == 200:
                print(bcolors.GREEN + str(response.code) + ' ' + bcolors.ENDC + url + line)
                check_source_leak(url, line)
        except urllib.request.HTTPError:
            pass

def check_source_leak(url, filename):
    """print source leak results"""
    leak1 = '.' + filename + '.swp'
    leak2 = '.' + filename + '.swo'
    leak3 = filename + '.bak'
    leak4 = filename + '~'
    leaks = [leak1, leak2, leak3, leak4]
    for leak in leaks:
        try:
            response = urllib.request.urlopen(url+leak)
            if response.code == 200:
                print(bcolors.GREEN + str(response.code) + ' ' + bcolors.ENDC + url + leak)
        except urllib.request.HTTPError:
            pass

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
        print("Usage: python3 main.py xxx.txt")

if __name__ == '__main__':
    main()
