import matplotlib.pyplot as plt
from matplotlib import *
import numpy as np
import scipy.stats as stats
#plt.style.use('dark_background')

# Importing required libraries

fig = plt.figure()

ax = fig.add_subplot(111)
x_min = 0.0
x_max = 16.0

mean = 8.0
std = 3.0

x_point=[8, 9]
y_point=[0.2, 0.1762]

x = np.linspace(x_min, x_max, 100)

y = stats.norm.pdf(x,mean,std)

#Plotting the Results
ax.plot(x, y,color='c',linewidth='3')
ax.plot(x, stats.norm.pdf(x,6,2),color='m',linewidth='3')
ax.set_xlim(x_min,x_max)
ax.set_ylim(0,0.23)
ax.grid(alpha=0.1)
ax.set_ylim(bottom=0)
fig.text(0.07, 0.85, r'$ \frac{dW}{ d v}$',fontsize=18, color='green')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.text(12.5, 0.06, r'$T_2$',fontsize=18, color='green')
ax.text(7.5, 0.17, r'$T_1$',fontsize=18, color='green')
ax.text(12, 0.18, r'$T_1 < T_2$',fontsize=18, color='green')
fig.text(0.9, 0.07, r'$v$',fontsize=18, color='green')
#ax.set_xticks([0,2,4,6,8,10,12,14])
ax.set_yticks([])
ax.set_xticks([])
plt.show()