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
    try:
        if sys.argv[1].startswith('-'):
            option = sys.argv[1][1:]
            if option == 'f':
                with open(sys.argv[2]) as f1:
                    urls = f1.read().splitlines()
                f1.close()
                for url in urls:
                    file_scan(url)
                    dir_scan(url)
            elif option == 'u':
                url = sys.argv[2]
                file_scan(url)
                dir_scan(url)
            else:
                print("Error: 未知参数")
                exit()
        else:
            print("Usage: python main.py -u http://xxx.xxx/ 独立")
            print("       python main.py -f xxx.txt 批量")
    except Exception as e:
        print("Usage: python main.py -u http://xxx.xxx/ 独立")
        print("       python main.py -f xxx.txt 批量")

if __name__ == '__main__':
    main()
