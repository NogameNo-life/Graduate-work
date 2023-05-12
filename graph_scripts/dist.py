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
ax.plot(x, y,color='blue',linewidth='4')

ax.set_xlim(x_min,x_max)
ax.set_ylim(0,0.23)
ax.grid(alpha=0.1)
ax.set_ylim(bottom=0)
fig.text(0.08, 0.8, r'$ \frac{\Delta n}{ \Delta v}$',fontsize=15, color='green')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_yticks([])
fig.text(0.5, 0.07, r'$c$',fontsize=15, color='green')
fig.text(0.56, 0.07, r'$v_{ср}$',fontsize=15, color='green')
fig.text(0.85, 0.07, r'$v$',fontsize=15, color='green')
ax.set_xticks([])
X = [0.5, 0.07]
Y = [7.81, 0.2011]

ax.vlines(8, 0, 0.2, color='#8F00FF')
ax.vlines(9, 0, 0.1762, color='blue')
ax.scatter(x_point, y_point, s=30,marker='o',color='coral', zorder=3)

plt.show()