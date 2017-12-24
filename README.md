# ctf web scan

CTF中web源码泄露扫描

## Description

使用python的requests，功能比较简单，字典有待完善。
目前只支持php。

## Usage

将待扫描的所有url（以`/`结尾）加入`xxx.txt`。

``` bash
python2 main.py xxx.txt
python3 main.py xxx.txt
```
