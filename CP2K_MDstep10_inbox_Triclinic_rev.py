#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import math  
import itertools 
import numpy as np
import random
import scipy


def abcangle2abcvector(Cellabc,alpha,beta,gamma):
    global va
    global vb
    global vc
    alpharad = alpha*math.pi/180.0
    betarad = beta*math.pi/180.0
    gammarad = gamma*math.pi/180.0
    va=np.array([1.0,0.0,0.0])*Cellabc[0]
    vnbx=round(math.cos(gammarad),10)
    vnby=math.sqrt(1.0-vnbx**2)
    vb=np.array([vnbx,vnby,0.0])*Cellabc[1]
    vncx=round(math.cos(betarad),10)
    vncy=round((math.cos(alpharad)-math.cos(alpharad)*math.cos(betarad))/math.sin(alpharad),10)
    vncz=math.sqrt(1.0-vncx**2-vncy**2)
    vc=np.array([vncx,vncy,vncz])*Cellabc[2]

def transferxyz2abc(xyz,Vtransmatrix):
    abc=np.linalg.solve(Vtransmatrix,xyz)
#set the periodic condition
    abc=abc%1.0
    return abc

def transferabc2xyz(abc,Vtransmatrix):
    xyz=np.dot(Vtransmatrix,abc)
    return xyz

# 打开一个文件
fo = open("test-pos-1.xyz")
print("是否已关闭 : ", fo.closed)
print("访问模式 : ", fo.mode)
#print("末尾是否强制加空格 : ", fo.softspace)
print("#########MODE_CHOICE#########")
#For only output
#MODECHOICE=0
#For md trajectories with step cut.
MODECHOICE=1
#Set the cut step for MD
MDsteopcut=10
if MODECHOICE==0:
    print("OUTPUT mode, only output the last step in the cell!")
    outfilename="out.xyz"
elif MODECHOICE==1:
    print("MD trajectory mode, output ever cut step with a step size of %d"%MDsteopcut)
    outfilename="MD_inBox_step10.xyz"
else:
    print("EORROR! MODECHOICE should be 0 or 1! No it is %d"%MODECHOICE)
    exit(1)
#open the output file
fa = open(outfilename, "w")

#input the lattice constances
print("Here in mode of abc with alpha,beta,gamma,please check or correct the numbers below.")
Cellabc=np.array([28.0,28.0,28.0])
alpha=90.0
beta=90.0
gamma=90.0
print("a,b,c length:", Cellabc)
print("alpha,beta,gamma:(in degree)",alpha,beta,gamma)
print("Transfering abc with alpha,beta,gamma to lattice vectors...")
va=np.array([0.0,0.0,0.0])
vb=np.array([0.0,0.0,0.0])
vc=np.array([0.0,0.0,0.0])
abcangle2abcvector(Cellabc,alpha,beta,gamma)
#input the lattice constances, way2
#print("Here in mode of lattice vectors,please check or correct the numbers below.")
#va=np.array([13.5518,0.0,0.0])
#vb=np.array([6.52081,13.1092,0.0])
#vc=np.array([0.0,0.0,31.9782])
#check the lattice vectors
print("Check the corresponding lattice vector below:")
print("Va", va)
print("Vb", vb)
print("Vc", vc)
print("#########CHECK the lattice vector and pressure any botton!#####")
input()
# Set Vtransmatrix, it is the reverse matrix of [va, vb, vc]
Vtransmatrix=np.array([va, vb, vc]).T
#Read lines
array = fo.readlines()
linenum = len(array)
#print "WaterCount=" , WCount
print("文件行数 : ", linenum)
Line = array[0].split()
print("is digit:", (Line[0].isdigit()))
if Line[0].isdigit()==True :
    Na = int(Line[0])
    blocks = int(linenum/(Na+2))
    print("blocks = %d" %blocks)
    if MODECHOICE==1:
        for nb in range(0,blocks,1):
            i0 = nb*(Na+2)+1
            Line = array[i0].split()
            stepnumstring=Line[2]
            stepnumstring=stepnumstring[:-1]
#            print(stepnumstring)
            stepnumhere=int(stepnumstring)
#            print(stepnumhere)
#            input()
            if(stepnumhere%MDsteopcut==0):
                fa.write("%s" % array[(nb*(Na+2))])
                fa.write("%s" % array[(nb*(Na+2)+1)])
                i0 = nb*(Na+2)+2
                for i in range(0,Na):
                    j=i0+i   
                    Line = array[j].split()
                    if len(Line)!=4 :
                        break
                    xyz=np.array([float(Line[1]),float(Line[2]),float(Line[3])])
                    abc=transferxyz2abc(xyz,Vtransmatrix)
                    xyznew=transferabc2xyz(abc,Vtransmatrix)
                    fa.write("%s   %.10f   %.10f   %.10f   \n" % (Line[0], xyznew[0], xyznew[1], xyznew[2]))
    #MODECHOICE=0
    else:
        nb=blocks-1
        fa.write("%s" % array[(nb*(Na+2))])
        fa.write("%s" % array[(nb*(Na+2)+1)])
        i0 = nb*(Na+2)+2
        for i in range(0,Na):
            j=i0+i   
            Line = array[j].split()
            if len(Line)!=4 :
                break
            xyz=np.array([float(Line[1]),float(Line[2]),float(Line[3])])
            abc=transferxyz2abc(xyz,Vtransmatrix)
            xyznew=transferabc2xyz(abc,Vtransmatrix)
            fa.write("%s   %.10f   %.10f   %.10f   \n" % (Line[0], xyznew[0], xyznew[1], xyznew[2]))
else:
    print("ERROR! The first line is not number!")
    exit(1)
fo.close()
fa.close()

