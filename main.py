#coding:utf-8
#!/usr/bin/python3
"""ctf web scan
Author: D4rk
TODO: 针对某些全站200的情况，分析返回数据包匹配"404 not found 未找到页面"字样
"""

import sys
import argparse
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
        try:
            r = requests.get(url+line, timeout=1)
            if r.status_code == 200 or r.status_code == 403:
                print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
                # 如果扫描到存在的目录会进行敏感文件扫描
                file_scan(url+line)
        except requests.exceptions.ConnectionError:
            print("Error connecting to site \"%s\"" % url)
            sys.exit(1)

def file_scan(url):
    """扫描web敏感文件"""
    with open('dic.txt') as f:
        lines = f.read().splitlines()
    f.close()
    for line in lines:
        try:
            r = requests.get(url+line, timeout=1)
            if r.status_code == 200:
                print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + line)
                # 如果扫描到存在敏感文件会进行编辑器源码泄露扫描
                source_scan(url, line)
        except requests.exceptions.ConnectionError:
            print("Error connecting to site \"%s\"" % url)
            sys.exit(1)

def source_scan(url, filename):
    """扫描编辑器源码泄露"""
    leaks = ['.%s.swp' % filename,
             '.%s.swo' % filename,
             '%s.bak' % filename,
             '%s~' % filename]
    for leak in leaks:
        try:
            r = requests.get(url+leak, timeout=1)
            if r.status_code == 200:
                print(bcolors.GREEN + str(r.status_code) + ' ' + bcolors.ENDC + url + leak)
        except requests.exceptions.ConnectionError:
            print("Error connecting to site \"%s\"" % url)
            sys.exit(1)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="CTF Web Scan")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Specify file name")
    group.add_argument("-u", "--url", help="Specify target url")
    if len(sys.argv) == 1:
        parser.print_usage(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if args.url:
        url = args.url
        file_scan(url)
        dir_scan(url)
        print(bcolors.GREEN + 'Scan Complete: %s'%url + bcolors.ENDC)
    elif args.file:
        with open(args.file) as f1:
            urls = f1.read().splitlines()
        f1.close()
        for url in urls:
            file_scan(url)
            dir_scan(url)
            print(bcolors.GREEN + 'Scan Complete: %s'%url + bcolors.ENDC)
        sys.exit(1)
    else:
        parser.print_usage(sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
