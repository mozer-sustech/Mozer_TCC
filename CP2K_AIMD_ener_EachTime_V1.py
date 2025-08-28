#!/usr/bin/python
# -*- coding: UTF-8 -*-
#Process .ener file,Writen by WeiCAO#
#Version 1.0 WildCard mode Update22/12/13##


from numpy import *
import matplotlib.pyplot as plt
import glob

en=glob.glob(r'.\*.ener')

for f in en:
    fo = open(f,'r')
    array = fo.readlines()
    Linenum = len(array)
    print("文件行数 : ", Linenum)

#Read lines
    x = []
    y = []
    for num in range(1,Linenum):
        Line = array[num].strip('\n').split()
        x.append(float(Line[0]))
        y.append(float(Line[-1]))

    plt.xlabel('AIMD Step')
    plt.ylabel('Time Cost/s')
    # print(x)
    Average_Time_Cost=round(sum(y)/len(x))
    print("平均每步耗时为：%f s"%Average_Time_Cost)
    plt.plot(x,y,label = 'Average Time Cost: %f s'%Average_Time_Cost)
    fo.close()
    plt.legend()

    plt.show()

    input("按回车退出")
    input("按三下就退出，2")
    input("按三下就退出，3")