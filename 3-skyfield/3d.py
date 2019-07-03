import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from skyfield.api import load
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle

np.random.seed(19680801)
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
ax.legend()
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])
ax.set_zlim(0, 1), ax.set_zticks([])

n_drops = 10
rain_drops = np.zeros(n_drops, dtype=[('position', float, 3),
                                      ('color',    float, 4)])
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1], rain_drops['position'][:, 2])
def update(frame_number):
    global scat
    scat.remove()
    rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 3))
    scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1], rain_drops['position'][:, 2])
    current_index = frame_number % n_drops
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)
    rain_drops['position'][current_index] = np.random.uniform(0, 1, 3)
    rain_drops['color'][current_index] = (0, 0, 0, 1)
    scat.set_edgecolors(rain_drops['color'])

animation = FuncAnimation(fig, update, interval=2000)
plt.show()
