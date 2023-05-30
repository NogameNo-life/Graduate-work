import numpy as np
from scipy.spatial.distance import pdist, squareform

class Particle:

    def __init__(self, pos, vel, r, m):
        """
        Initialize the simulation with identical, circular particles of radius
        r and mass m. The n x 2 state arrays pos and vel hold the n particles'
        positions in their rows as (x_i, y_i) and (vx_i, vy_i).
        """

        self.pos = np.asarray(pos, dtype=float)
        self.vel = np.asarray(vel, dtype=float)
        self.n = self.pos.shape[0]
        self.r = r
        self.m = m
        self.nsteps = 0

    def advance(self, dt):
        """Advance the simulation by dt seconds."""
        X, Y = 0, 1
        self.nsteps += 1
        # Update the particles' positions according to their velocities.
        self.pos += self.vel * dt*0.1
        # Find indices for all unique collisions.
        dist = squareform(pdist(self.pos))
        iarr, jarr = np.where(dist < 2 * self.r)
        k = iarr < jarr
        iarr, jarr = iarr[k], jarr[k]

        # For each collision, update the velocities of the particles involved.
        for i, j in zip(iarr, jarr):
            pos_i, vel_i = self.pos[i], self.vel[i]
            pos_j, vel_j =  self.pos[j], self.vel[j]
            rel_pos, rel_vel = pos_i - pos_j, vel_i - vel_j
            r_rel = rel_pos @ rel_pos
            v_rel = rel_vel @ rel_pos
            v_rel = 2 * rel_pos * v_rel / r_rel - rel_vel
            v_cm = (vel_i + vel_j) / 2
            self.vel[i] = v_cm - v_rel/2
            self.vel[j] = v_cm + v_rel/2

        # Bounce the particles off the walls where necessary, by reflecting
        # their velocity vectors.
        hit_left_wall = self.pos[:, X] < self.r
        hit_right_wall = self.pos[:, X] > 1 - self.r
        hit_bottom_wall = self.pos[:, Y] < self.r
        hit_top_wall = self.pos[:, Y] > 1 - self.r
        self.vel[hit_left_wall | hit_right_wall, X] *= -1
        self.vel[hit_bottom_wall | hit_top_wall, Y] *= -1

