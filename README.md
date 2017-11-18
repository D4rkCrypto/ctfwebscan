# ctf web scan

CTF中web源码泄露扫描

## Description

使用python3的urllib实现，功能比较简单，字典有待完善。
目前只支持php。

## Usage

将待扫描的所有url（以`/`结尾）加入`xxx.txt`。

``` bash
python3 main.py xxx.txt
```
