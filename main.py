#!/usr/bin/python3
"""ctf web scan
Author: D4rk
"""

import sys
import urllib.request
import urllib.parse

def scan(url):
    """print all scanned results"""
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
                print('[+] '+url+leak)
        except urllib.request.HTTPError:
            pass

def main():
    """main function"""
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f1:
            webs = f1.read().splitlines()
        f1.close()
        for web in webs:
            scan(web)
    else:
        print("Usage: python3 main.py xxx.txt")

if __name__ == '__main__':
    main()
    