# -*- coding:utf-8 -*-
import chardet

a = b"\346\262\241\346\234\211\346\217\217\350\277\260"

fencoding = chardet.detect(a)
print(fencoding)
a = a.decode('utf-8')
print(a)