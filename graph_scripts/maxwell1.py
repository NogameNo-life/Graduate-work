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
std = 2.0

x_point=[8, 9]
y_point=[0.2, 0.1762]

x = np.linspace(x_min, x_max, 100)

y = stats.norm.pdf(x,mean,std)

#Plotting the Results
ax.plot(x, y,color='c',linewidth='3')
ax.set_xlim(x_min,x_max)
ax.set_ylim(0,0.23)
ax.set_ylim(bottom=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.text(8.5, 0.21, r'$ \frac{dW}{ dv_x}$',fontsize=18, color='green')
fig.text(0.9, 0.07, r'$v_x$',fontsize=18, color='green')
ax.set_xticks([])
ax.set_yticks([])
ax.vlines(8, 0, 0.23, color='black',linewidth=1)
plt.show()