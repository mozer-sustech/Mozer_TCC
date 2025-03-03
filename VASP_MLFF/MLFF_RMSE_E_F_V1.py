############Post Process of MLFF Outputs Files##############
#1.Extract data from ML_ABN and ML_REG
#2.Get E_reg_test.dat, F_reg_test.dat, Stress_reg_test.dat
#Note: 1 and 2 are accomplished by Parse_MLFF_REGFile.sh 

#3.Visualize E_DFT_ML, F_DFT_ML
#4.Summarize RMSE & MAE of E & F.

##################Visualize the difference of E/F between DFT and ML
import numpy as np
import matplotlib.pyplot as plt

def rmse(dft, ml):
    return np.sqrt(((dft - ml) ** 2).mean())

def mae(dft, ml):
    return np.sum(np.abs(dft -  ml))/len(dft)

E = np.loadtxt('E_reg.dat')
F = np.loadtxt('F_reg.dat')
S = np.loadtxt('Stress_reg.dat')
print(F.shape)


#norms of forces
F_dft = np.sum(np.abs(F[:,0].reshape((-1,3)))**2,axis=-1)**(1./2)
F_ml = np.sum(np.abs(F[:,1].reshape((-1,3)))**2,axis=-1)**(1./2)

#RMSE
RMSE_E = 1000*rmse(E[:,0], E[:,1]) #in meV/atom
RMSE_F = 1000*rmse(F_dft, F_ml) #in meV/Å
RMSE_Stress = rmse(S[:,0], S[:,1])
#MAE
MAE_E = mae(E[:,0], E[:,1])
MAE_F =mae(F_dft, F_ml)
MAE_Stress = mae(S[:,0], S[:,1])

print("     MAE ,        RMSE,          max (absolute) error")
print("energy (meV/at.):")
print( "{:10.4f}".format(1000*MAE_E ),
       "{:10.4f}".format(RMSE_E),
       "{:10.4f}".format(1000*max(np.abs(E[:,0] - E[:,1]))) )
print("stress (kbar):")
print( "{:10.4f}".format(MAE_Stress),
       "{:10.4f}".format(RMSE_Stress),
       "{:10.4f}".format(max(np.abs(S[:,0] - S[:,1]))) )
print("force components (eV/A):")
print( "{:10.4f}".format(mae(F[:,0], F[:,1])),
       "{:10.4f}".format(rmse(F[:,0], F[:,1])),
       "{:10.4f}".format(max(np.abs(F[:,0] - F[:,1]))) )
print("force norm (meV/A):")
print( "{:10.4f}".format(MAE_F ),
       "{:10.4f}".format(RMSE_F),
       "{:10.4f}".format(max(np.abs(F_dft - F_ml))))


from sklearn.metrics import r2_score
x = E[:, 0]
y = E[:, 1]

m, b = np.polyfit(x, y, 1)  
y_pred = m * x + b
r2 = r2_score(y, y_pred)

Color_A= (77/256,134/256, 169/256)
Color_B= (205/256,82/256, 142/256)



###########Plot of RMSE_E
plt.subplot(1,2,1)
plt.scatter(x, y,color=Color_A) #,  edgecolors='k', label='Data', , s=50, alpha=0.7
plt.plot(x, y_pred, color=Color_B, linewidth=2,linestyle=':') #label=f'Linear Fit', 
RMSE_text = f'$RMSE\_E = {RMSE_E:.3f} \\text{{ meV/atom}}$'
plt.text(0.5, 0.2, RMSE_text, transform=plt.gca().transAxes, fontsize=12, 
        verticalalignment='top') #, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
plt.xlabel("E (DFT/eV)", fontsize=14, fontname='Arial')
plt.ylabel("E (ML/eV)", fontsize=14, fontname='Arial')
# plt.xticks( fontname='Arial')
# plt.yticks( fontname='Arial')


###########Plot of RMSE_F
x1 = F[:,0]
y1 = F[:,1]
m1, b1 = np.polyfit(x1, y1, 1)  
y1_pred = m1 * x1 + b1
plt.subplot(1,2,2)
plt.scatter(x1, y1,color=Color_A, s=50, alpha=0.7) #,  edgecolors='k', label='Data', 
plt.plot(x1, y1_pred, color=Color_B, linewidth=2,linestyle=':') #label=f'Linear Fit', 

RMSE_text = f'$RMSE\_F = {RMSE_F:.3f} \\text{{ meV/Å}}$'
plt.text(0.5, 0.2, RMSE_text, transform=plt.gca().transAxes, fontsize=12, 
        verticalalignment='top') #, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
plt.xlabel("F (DFT/eV)", fontsize=14, fontname='Arial')
plt.ylabel("F (ML/eV)", fontsize=14, fontname='Arial')


plt.legend(frameon=False, fontsize=12)
plt.show()

