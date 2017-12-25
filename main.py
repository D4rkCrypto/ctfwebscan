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
    """扫描web敏感目录"""
    with open('dir.txt') as f:
        lines = f.read().splitlines()
    f.close()

    for line in lines:
        r = requests.get(url+line)
        if r.status_code == 200 or r.status_code == 403:
            print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
            # 如果扫描到存在的目录会进行敏感文件扫描
            file_scan(url+line)

def file_scan(url):
    """扫描web敏感文件"""
    with open('dic.txt') as f:
        lines = f.read().splitlines()
    f.close()

    for line in lines:
        r = requests.get(url+line)
        if r.status_code == 200:
            print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
            # 如果扫描到存在敏感文件会进行编辑器源码泄露扫描
            source_scan(url, line)

def source_scan(url, filename):
    """扫描编辑器源码泄露"""
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
    """主函数"""
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
