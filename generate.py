#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File    :   generate.py
@Time    :   2020/05/16 11:51:48
@Author  :   ryanxjli 
@Desc    :   根据目录结构自动生成笔记的目录（按目录结构，tag, time）
'''

# here put the import lib
import os
from datetime import datetime
import traceback
from typing import List


class Global(object):
    SPACE = '&emsp;&emsp;&emsp;&emsp;'
    ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
    # 按tag
    MTAG = {}
    # 按date
    MDATE = {}
    COMMENT_INFO = '''
# 个人笔记
## 说明
1. images统一存放图片资源
2. 笔记文件必须要有头信息， 头信息如下：
        
        ---
        title: xxxx
        date: 2016-09-05 15:58:50
        tags: C++,python
        ---
3. 每次提交前运行generate.py重新生成目录信息
4. push后自动调用github actions

## 按目录
'''


class PostInfo(object):

    def __init__(self, title : str, date : str, tags : str):
        self.title = title
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.tags = [t.strip() for t in tags.split(",")]

    def __str__(self):
        tags = ','.join(self.tags)
        return "{}\t{}\t{}".format(self.title, self.date, tags)


def ParsePostFile(file : str):
    title, line, tags = None, None, None
    with open(file, 'r') as f:
        line = f.readline()
        while line and (not line.startswith('---')):
            line = f.readline()
        line = f.readline()
        if line:
            title = line.split(':', maxsplit=1)[1].strip()
        line = f.readline()
        if line:
            date = line.split(':', maxsplit=1)[1].strip()
        line = f.readline()
        if line:
            tags = line.split(':', maxsplit=1)[1].strip()
    if (title == None) or (date == None) or (tags == None):
        return None
    return PostInfo(title, date, tags)
    

def AddToMTag(info : PostInfo, strinfo : str):
    # 根据tag添加
    for tag in info.tags:
        if tag not in Global.MTAG:
            Global.MTAG[tag] = []
        Global.MTAG[tag].append(strinfo)


def WriteMTag():
    tagpath = 'generated/tags'
    # 清理旧文件
    if os.path.exists(tagpath):
        os.system('rm -rf {}/*'.format(tagpath))
    if not os.path.exists(tagpath):
        os.makedirs(tagpath)
    # 创建tags目录, 并写根目录readme
    for key, value in Global.MTAG.items():
        tagdir = os.path.join(tagpath, key)
        os.mkdir(tagdir)
        with open(os.path.join(tagdir, 'README.md'), 'w') as f:
            strinfo = "[..]({})<br/><br/>\n".format("/README.md")
            f.write(strinfo)
            f.writelines(value)
    # 写根目录readme
    with open('README.md', 'a') as f:
        f.write('## 按tag\n')
        for key in Global.MTAG.keys():
            tagdir = os.path.join("/{}".format(tagpath), key)
            strinfo = "[{}]({})<br/><br/>\n".format(key, os.path.join(tagdir, "README.md"))
            f.write(strinfo)


def AddToMDate(info : PostInfo, strinfo : str):
    # 按年月添加
    datekey = '{}年{}月'.format(info.date.year, info.date.month)
    if datekey not in Global.MDATE:
        Global.MDATE[datekey] = []
    Global.MDATE[datekey].append(strinfo)
    pass


def WriteMDate():
    datepath = 'generated/date'
    # 清理旧文件
    if os.path.exists(datepath):
        os.system('rm -rf {}/*'.format(datepath))
    if not os.path.exists(datepath):
        os.makedirs(datepath)
    # 创建tags目录, 并写根目录readme
    for key, value in Global.MDATE.items():
        tagdir = os.path.join(datepath, key)
        os.mkdir(tagdir)
        with open(os.path.join(tagdir, 'README.md'), 'w') as f:
            strinfo = "[..]({})<br/><br/>\n".format("/README.md")
            f.write(strinfo)
            f.writelines(value)
    # 写根目录readme
    with open('README.md', 'a') as f:
        f.write('## 按日期\n')
        for key in Global.MDATE.keys():
            tagdir = os.path.join("/{}".format(datepath), key)
            strinfo = "[{}]({})<br/><br/>\n".format(key, os.path.join(tagdir, "README.md"))
            f.write(strinfo)
    pass
     

def GenerateByDir(path : str):
    
    dirlist = []
    filelist = []

    # 父目录处理
    if path != Global.ROOT_DIR:
        dirname = os.path.dirname(path)[len(Global.ROOT_DIR):]
        if dirname == '':
            dirname = '/'
        strinfo = "[..]({})<br/><br/>\n".format(os.path.join(dirname, "README.md"))
        dirlist.append(strinfo)
    # 根目录， 添加额外说明信息
    else:
        dirlist.append(Global.COMMENT_INFO)

    # 递归生成readme, 先生成子目录，再生成父目录
    for dir_file in os.listdir(path):
        if ((dir_file == "images") and os.path.isdir(dir_file)) or \
            (dir_file == "README.md") or \
            dir_file.startswith('.') or \
            ((dir_file == "generated") and os.path.isdir(dir_file)) or \
            (dir_file.endswith('.py')):
            continue
        dir_file_path = os.path.join(path, dir_file)
        print(dir_file_path)
        if os.path.isdir(dir_file_path):
            GenerateByDir(dir_file_path)
            strinfo = "[{}]({})<br/><br/>\n".format(dir_file, os.path.join(dir_file_path[len(Global.ROOT_DIR):], "README.md"))
            dirlist.append(strinfo)
        else:
            if not dir_file.endswith('.md'):
                continue
            info : PostInfo = ParsePostFile(dir_file_path)
            if info == None:
                continue
            strinfo = "[{}]({}){}发布时间：{}{}标签：{}<br/><br/>\n".format(
                info.title, dir_file_path[len(Global.ROOT_DIR):], Global.SPACE, 
                info.date.strftime('%Y-%m-%d %H:%M:%S'), Global.SPACE, 
                ','.join(info.tags))
            filelist.append(strinfo)
            AddToMTag(info, strinfo)
            AddToMDate(info, strinfo)


    # 写readme文件
    readmefile = os.path.join(path, 'README.md')
    with open(readmefile, 'w') as f:
        f.writelines(dirlist)
        f.writelines(filelist)



def main():
    try:
        print("scan dir: {}".format(Global.ROOT_DIR))
        GenerateByDir(Global.ROOT_DIR)
        WriteMTag()
        WriteMDate()
        
    except Exception:
        print(traceback.format_exc())
    pass

if __name__ == '__main__':
    main()