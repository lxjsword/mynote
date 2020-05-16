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
        strinfo = '''# 个人笔记
说明
1. images统一存放图片资源
2. 笔记文件必须要有头信息， 头信息如下：
        
        ---
        title: xxxx
        date: 2016-09-05 15:58:50
        tags: C++,python
        ---

        '''
        dirlist.append(strinfo)
    # 递归生成readme, 先生成子目录，再生成父目录
    for dir_file in os.listdir(path):
        if (dir_file == "images") or (dir_file == "README.md") or dir_file.startswith('.'):
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

    # 写readme文件
    readmefile = os.path.join(path, 'README.md')
    with open(readmefile, 'w') as f:
        f.writelines(dirlist)
        f.writelines(filelist)



def main():
    try:
        print("scan dir: {}".format(Global.ROOT_DIR))
        GenerateByDir(Global.ROOT_DIR)
        
    except Exception as e:
        print(traceback.format_exc())
    pass

if __name__ == '__main__':
    main()