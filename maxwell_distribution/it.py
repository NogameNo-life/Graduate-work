import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from itertools import combinations
from histogram import Histogram
from particle import Particle

class Simulation:

    def __init__(self, n, radius=0.01, styles=None):

        self.init_particles(n, radius, styles)

    def init_particles(self, n, radius, styles=None):
        """Initialize the n Particles of the simulation.

        Positions and velocities are chosen randomly; radius can be a single
        value or a sequence with n values.

        """

        try:
            iterator = iter(radius)
            assert n == len(radius)
        except TypeError:
            # r isn't iterable: turn it into a generator that returns the
            # same value n times.
            def r_gen(n, radius):
                for i in range(n):
                    yield radius
            radius = r_gen(n, radius)

        self.n = n
        self.particles = []
        for i, rad in enumerate(radius):
            # Try to find a random initial position for this particle.
            while True:
                # Choose x, y so that the Particle is entirely inside the
                # domain of the simulation.
                x, y = rad + (1 - 2*rad) * np.random.random(2)
                # Choose a random velocity (within some reasonable range of
                # values) for the Particle.
                vr = 0.1 * np.random.random() + 0.05
                vphi = 2*np.pi * np.random.random()
                vx, vy = vr * np.cos(vphi), vr * np.sin(vphi)
                particle = Particle(x, y, vx, vy, rad, styles)
                # Check that the Particle doesn't overlap one that's already
                # been placed.
                for p2 in self.particles:
                    if p2.overlaps(particle):
                        break
                else:
                    self.particles.append(particle)
                    break

    def handle_collisions(self):
        """Detect and handle any collisions between the Particles.

        When two Particles collide, they do so elastically: their velocities
        change such that both energy and momentum are conserved.

        """

        def change_velocities(p1, p2):
            """
            Particles p1 and p2 have collided elastically: update their
            velocities.

            """

            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = p1.r, p2.r
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = p1.v, p2.v
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.v = u1
            p2.v = u2

        # We're going to need a sequence of all of the pairs of particles when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.particles list of Particles on the fly.
        pairs = combinations(range(self.n), 2)
        for i,j in pairs:
            if self.particles[i].overlaps(self.particles[j]):
                change_velocities(self.particles[i], self.particles[j])

    def advance_animation(self, dt):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.particles):
            p.advance(dt)
            self.circles[i].center = p.r
        self.handle_collisions()
        return self.circles

    def advance(self, dt):
        """Advance the animation by dt."""
        for i, p in enumerate(self.particles):
            p.advance(dt)
        self.handle_collisions()

    def init(self):
        """Initialize the Matplotlib animation."""

        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.sim_ax))
        return self.circles, self.speed_hist.patch

    def animate(self, i):
        """The function passed to Matplotlib's FuncAnimation routine."""

        self.advance_animation(0.01)
        self.speed_hist.update(self.data)
        return self.circles, self.speed_hist.patch

    def do_animation(self, save=False):
        """Set up and carry out the animation of the molecular dynamics.

        To save the animation as a MP4 movie, set save=True.
        """

        rscale = 5.e6
        # Scale time by this factor, in s-1.
        tscale = 1e9    # i.e. time will be measured in nanoseconds.
        # Take the mean speed to be the root-mean-square velocity of Ar at 300 K.
        self.sbar = 353 * rscale / tscale
        fig, self.sim_ax = plt.subplots()
        fig.subplots_adjust(left=0, right=0.97)
        self.sim_ax = fig.add_subplot(121, aspect='equal', autoscale_on=False)
        self.sim_ax.set_xticks([])
        self.sim_ax.set_yticks([])
        # Make the box walls a bit more substantial.
        for spine in self.sim_ax.spines.values():
           spine.set_linewidth(2)

        self.speed_ax = fig.add_subplot(122)
        self.speed_ax.set_xlabel('Speed $v\,/m\,s^{-1}$')
        self.speed_ax.set_ylabel('$f(v)$')
        #self.speed_ax.set_xlim(speed_hist.left[0], speed_hist.right[-1])
        # TODO don't hardcode the upper limit for the histogram speed axis.
        ticks = np.linspace(0, 600, 7, dtype=int)
        self.speed_ax.set_xticks(ticks * rscale/tscale)
        self.speed_ax.set_xticklabels([str(tick) for tick in ticks])
        self.speed_ax.set_yticks([])
        mu, sigma = 0, 0.1
        self.data = np.random.normal(mu, sigma, 1000)
        self.speed_hist = Histogram(self.data, mu,50, density=True)
        self.speed_hist.draw(self.speed_ax)

        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init,
                               frames=800, interval=2, blit=True)
        plt.show()


if __name__ == '__main__':
    nparticles = 50
    radii = np.random.random(nparticles)*0.03+0.02
    styles = {'edgecolor': 'C0', 'linewidth': 2, 'fill': None}
    sim = Simulation(nparticles, radii, styles)
    sim.do_animation(save=False)