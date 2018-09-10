# -*- coding:utf-8 -*-
import os, sys

rootdir = 'D:/report/20180821'
for dirpath, dirnames, filenames in os.walk(rootdir):
    # print('Directory', dirpath)
    for filename in filenames:
        # print(filename)
        with open(rootdir + '/' + filename,'r',encoding='gbk') as f:
            for line in f:
                if 'security' in line:
                    print(filename)
