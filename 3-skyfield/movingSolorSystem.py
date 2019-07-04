#coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from skyfield.api import load
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle

def sincos(planets, p1, p2):
    pla1, pla2 = planets[p1], planets[p2]
    ts = load.timescale()
    t = ts.now()
    astrometric = pla1.at(t).observe(pla2)
    ra, dec, distance = astrometric.radec()
    x = distance.au * math.cos(ra.radians)
    y = distance.au * math.sin(ra.radians)
    r = distance.au * math.cos(dec.radians)
    z = distance.au * math.sin(dec.radians)
    #print(x)
    #print('赤経 (right ascension, RA) :' + str(ra))
    #print('赤経：天体と春分点との角度の隔たりを東方向を正にとって表す。 ')
    #print('')
    #print(dec.radians)
    #print('赤緯 (declination, Dec) ：' + str(dec))
    #print('赤緯：天体と天の赤道の間の角度の隔たりを表す')
    #print('')
    #print(distance)
    print('')
    return [x, y, z, r]

def createMap():
    planets = load('de421.bsp')
    #print(planets)
    ret = [[0.0, 0.0, 0.0, 0.0]]
    ret.append(sincos(planets, 'sun', 'mercury'))
    ret.append(sincos(planets, 'sun', 'venus'))
    ret.append(sincos(planets, 'sun', 'earth'))
    ret.append(sincos(planets, 'sun', 'mars'))
    #ret.append(sincos(planets, 'sun', 'JUPITER BARYCENTER'))
    #ret.append(sincos(planets, 'sun', 'SATURN BARYCENTER'))
    #ret.append(sincos(planets, 'sun', 'URANUS BARYCENTER'))
    #ret.append(sincos(planets, 'sun', 'NEPTUNE BARYCENTER'))
    x = [x[0] for x in ret]
    y = [x[1] for x in ret]
    z = [x[2] for x in ret]
    r = [x[3] for x in ret]
    c = ['red', 'blue', 'yellow', 'cyan', 'magenta', 'green', 'green']
    c = c[:len(x)]
    return x, y, z, r, c

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')
#ax.legend()
hosei = 1.5
ax.set_xlim(-1.0 * hosei, hosei)
ax.set_ylim(-1.0 * hosei, hosei)
ax.set_zlim(-1.0 * hosei, hosei)
x, y, z, r, c = createMap()
scat = ax.scatter(x, y, z, c=c)
scat.set_sizes([40]*len(x))
i = 0
for rr in r:
    q=Circle((0, 0), rr, ec=c[i], fill=False)
    ax.add_patch(q)
    art3d.pathpatch_2d_to_3d(q, z=0, zdir="z")
    i += 1

def update(frame_number):
    global scat
    scat.remove()
    x, y, z, r, c = createMap()
    scat = ax.scatter(x, y, z, c=c)
    scat.set_sizes([40]*len(x))

animation = FuncAnimation(fig, update, interval=2000)
plt.show()
