# ctf web scan

CTF中web源码泄露扫描

## Description

使用python的requests，功能比较简单，字典有待完善。
目前只支持php。

## Feature

### 支持扫描类型

- 源码包 - `www.zip` `code.tar.gz` ...
- 敏感文件 - `admin.php` `flag.php` ...
- 敏感目录 - `/admin` `/upload` ...
- 编辑器源码备份 - `xxx.php~` `xxx.php.bak` `.xxx.php.swp` `.xxx.php.swo`

### 扫描过程

- 对源码包进行扫描
- 对敏感文件进行扫描
- 对已知敏感文件进行源码备份扫描
- 对敏感目录进行扫描
- 对已知目录下的敏感文件进行扫描
- 再进行源码备份扫描

## Usage

**所有url必须以`/`结尾**

``` bash
python main.py -u [url] 独立
python main.py -f [file] 批量
```

## Bugs

All known bugs:

- 批量扫描中，如果某一个网站请求错误，会直接exit