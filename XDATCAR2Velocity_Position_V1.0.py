#!/usr/bin/python3
# -*- coding: UTF-8 -*-
### Get Positions and Velocities of Specific Atom in AIMD Simulations
### For XDATCAR based on VASP
### Written by Wei Cao from SUSTech 2022.11.16 Version1.0 ###

import linecache
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import seaborn as sns

print("### Get Positions and Velocities of Specific Atom in AIMD Simulations ###")
print("### Process XDATCAR based on VASP ###")
print("### Written by Wei Cao from SUSTech 2022.11.16 Version1.0 ###")

file = open('XDATCAR', 'r+')
Target_Atom = input('Input the Number of Target Atom：')
linenum = int(Target_Atom) + 8  #Actual row of Atom in XDATCAR

#Get Cell ABC
Cella= linecache.getline('XDATCAR',3).strip('\n').split()
Cella= float(Cella[0])
Cellb= linecache.getline('XDATCAR',4).strip('\n').split()
Cellb= float(Cellb[1])
Cellc= linecache.getline('XDATCAR',5).strip('\n').split()
Cellc= float(Cellc[2])
print("Cell ABC：",Cella,Cellb,Cellc)
Cell_array=np.array([Cella,Cellb,Cellc])

#Get the Number of Total Atoms
Total_Atom_Number = linecache.getline('XDATCAR',7).strip('\n').split()
Total_Atom_Number= sum([int(a) for a in Total_Atom_Number]) #Get Number of Total Atoms in the System
print("Number of Total Atoms：",Total_Atom_Number)

##The Interval of AIMD Output
S1=linecache.getline('XDATCAR',8).strip('\n').split()[-1]
S2=linecache.getline('XDATCAR',8+Total_Atom_Number+1).strip('\n').split()[-1]
Time_Interval=int(S2)-int(S1)

def Target_Atom_Postion_AlongAIMD(x):  #get Target Atom Positions
    xyz_atom = linecache.getline('XDATCAR', x).strip('\n').split()
    xyz_atom = [float(a) for a in xyz_atom] #Note the Fractional Coordinate in XDATCAR
    Atom_Array_Fractional =np.array(xyz_atom)
    Atom_Array_Cartesian = Cell_array*Atom_Array_Fractional
    #print(Atom_Array_Cartesian)
    a=np.append(int(index),Atom_Array_Cartesian)   #Add Counting Number
    np.savetxt(f,np.atleast_2d(a),fmt="%3f")      #Load Array to txt

#Get the Positions of the Target Atom
index =1 #Counting for Each Structure in AIMD
with open('Possition_Atom%s.txt'%Target_Atom,'w+') as f:
    while linecache.getline('XDATCAR', linenum) != '':
        Target_Atom_Postion_AlongAIMD(linenum)
        index += 1  # Counting the order of Structures
        linenum = linenum + Total_Atom_Number + 1 #+1 for the leading row "Direct configuration="
f.close()
file.close()

#Pandas Process for Velocity Bases on Position
vel=pd.read_csv('Possition_Atom%s.txt'%Target_Atom,sep=' ', header=None, names=['order','x','y','z'])
vel['V_X']= (vel['x'].shift(-1) - vel['x'])/Time_Interval #v=Δx/t
vel['V_Y']= (vel['y'].shift(-1) - vel['y'])/Time_Interval
vel['V_Z']= (vel['z'].shift(-1) - vel['z'])/Time_Interval
vel.to_csv('Velocity_Atom%s.txt'%Target_Atom,columns=['V_X','V_Y','V_Z'],sep=' ') #Get Velocity output

#Data Visualization
Option1 = str(input("Output the Velocity Evolution?   y/n"))
if Option1== 'y':
    sns.pairplot(vel,x_vars=['order'],y_vars=['V_X','V_Y','V_Z']);#Output the Velocity Evolution
    plt.xlabel('AIMD/%sfs' % Time_Interval);
    plt.show();
else:
    print("No Velocity Output");


# sns.pairplot(vel,x_vars=['order'],y_vars=['V_X','V_Y','V_Z'])  #Velocity Evolution
# #sns.pointplot(data=vel,x='order',y='V_X')        #One of the Velocity Evolution in XYZ directions
# plt.xlabel('AIMD/%sfs'%Time_Interval) # ,fontsize = 20

#Directly Visualize via DataFrame
Option2=str(input("Output the Distribution?   y/n"))
if Option2== 'y':
    vel['V_X'].plot.density()  #KDE plot (Kernel Density Estimate)
    vel['V_Y'].plot.density()
    vel['V_Z'].plot.density()
else:
    print("No Distribution Output")
plt.show()

print("Position Output：Possition_Atom%s.txt"%(Target_Atom))
print("Velocity Output：Velocity_Atom%s.txt"%(Target_Atom))
input("Enter to Exit")
input(" ")