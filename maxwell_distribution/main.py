import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,  PillowWriter
from particle import Particle
from histogram import Histogram

plt.style.use('seaborn-dark')
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey

for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey

X, Y = 0, 1

# Number of particles.
n = 250
# Scaling factor for distance, m-1. The box dimension is therefore 1/rscale.
rscale = 5.e6
# Use the van der Waals radius of Ar, about 0.2 nm.
r = 2e-10 * rscale
# Scale time by this factor, in s-1.
tscale = 1e9    # i.e. time will be measured in nanoseconds.
# Take the mean speed to be the root-mean-square velocity of Ar at 300 K.
sbar = 353 * rscale / tscale
# Time step in scaled time units.
FPS = 30
dt = 1/FPS
# Particle masses, scaled by some factor we're not using yet.
m = 1
# Initialize the particles' positions randomly.
pos = np.random.random((n, 2))
# Initialize the particles velocities with random orientations and random
# magnitudes  around the mean speed, sbar.
theta = np.random.random(n) * 2 * np.pi
s0 = sbar * np.random.random(n)
vel = (s0 * np.array((np.cos(theta), np.sin(theta)))).T

sim = Particle(pos, vel, r, m)

# Set up the Figure and make some adjustments to improve its appearance.
DPI = 100
width, height = 1000, 500
fig = plt.figure(figsize=(width/DPI, height/DPI), dpi=DPI)
fig.subplots_adjust(left=0, right=0.97)
sim_ax = fig.add_subplot(121, aspect='equal', autoscale_on=False)
sim_ax.set_xticks([])
sim_ax.set_yticks([])
# Make the box walls a bit more substantial.
for spine in sim_ax.spines.values():
    spine.set_linewidth(2)

speed_ax = fig.add_subplot(122)
speed_ax.set_xlabel('Speed $v\,/m\,s^{-1}$')
speed_ax.set_ylabel('$f(v)$')

particles, = sim_ax.plot([], [], 'ko', color='#FE53BB')

def get_speeds(vel):
    """Return the magnitude of the (n,2) array of velocities, vel."""
    return np.hypot(vel[:, X], vel[:, Y])

def get_KE(speeds):
    """Return the total kinetic energy of all particles in scaled units."""
    return 0.5 * sim.m * sum(speeds**2)

speeds = get_speeds(sim.vel)
speed_hist = Histogram(speeds, 2 * sbar, 50, density=True)
speed_hist.draw(speed_ax)
speed_ax.set_xlim(speed_hist.left[0], speed_hist.right[-1])
# TODO don't hardcode the upper limit for the histogram speed axis.
ticks = np.linspace(0, 600, 7, dtype=int)
speed_ax.set_xticks(ticks * rscale/tscale)
speed_ax.set_xticklabels([str(tick) for tick in ticks])
speed_ax.set_yticks([])

fig.tight_layout()

# The 2D Maxwell-Boltzmann equilibrium distribution of speeds.
mean_KE = get_KE(speeds) / n
a = sim.m / 2 / mean_KE
# Use a high-resolution grid of speed points so that the exact distribution
# looks smooth.
sgrid_hi = np.linspace(0, speed_hist.bins[-1], 200)
f = 2 * a * sgrid_hi * np.exp(-a * sgrid_hi**2)
mb_line, = speed_ax.plot(sgrid_hi, f, c='0.7')
# Maximum value of the 2D Maxwell-Boltzmann speed distribution.
fmax = np.sqrt(sim.m / mean_KE / np.e)
speed_ax.set_ylim(0, fmax)

# For the distribution derived by averaging, take the abcissa speed points from
# the centre of the histogram bars.
sgrid = (speed_hist.bins[1:] + speed_hist.bins[:-1]) / 2
mb_est_line, = speed_ax.plot([], [], c='r')
mb_est = np.zeros(len(sgrid))

# A text label indicating the time and step number for each animation frame.
xlabel, ylabel = sgrid[-1] / 2, 0.8 * fmax
"""label = speed_ax.text(xlabel, ylabel, '$t$ = {:.1f}s, step = {:d}'.format(0, 0),
                     backgroundcolor='w')"""

def init_anim():
    """Initialize the animation"""
    particles.set_data([], [])

    return particles, speed_hist.patch, mb_est_line,# label

def animate(i):
    """Advance the animation by one step and update the frame."""
    global sim, verts, mb_est_line, mb_est
    sim.advance(dt)

    particles.set_data(sim.pos[:, X], sim.pos[:, Y])
    particles.set_markersize(10)

    speeds = get_speeds(sim.vel)
    speed_hist.update(speeds)

    # Once the simulation has approached equilibrium a bit, start averaging
    # the speed distribution to indicate the approximation to the Maxwell-
    # Boltzmann distribution.
    if i >= IAV_START:
        mb_est += (speed_hist.hist - mb_est) / (i - IAV_START + 1)
        mb_est_line.set_data(sgrid, mb_est)

   # label.set_text('$t$ = {:.1f} ns, step = {:d}'.format(i*dt, i))

    return particles, speed_hist.patch, mb_est_line, #label

# Only start averaging the speed distribution after frame number IAV_ST.
IAV_START = 200
# Number of frames; set to None to run until explicitly quit.
frames = 800
anim = FuncAnimation(fig, animate, frames=frames, interval=45, blit=False,
                    init_func=init_anim)
plt.show()