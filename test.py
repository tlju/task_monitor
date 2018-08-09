# -*- coding:utf-8 -*-
import datetime
a = 10
b = 20

while a < b:
    a += 1
    print(a)


date = datetime.datetime.now()

detester = date.strftime('%Y-%m-%d')

print(detester)