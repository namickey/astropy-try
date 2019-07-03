#coding: utf-8
import math
from skyfield.api import load
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from matplotlib import animation

def sincos(planets, p1, p2):
    pla1, pla2 = planets[p1], planets[p2]
    ts = load.timescale()
    t = ts.now()
    astrometric = pla1.at(t).observe(pla2)
    ra, dec, distance = astrometric.radec()

    print(p2)
    x = distance.au * math.cos(ra.radians)
    y = distance.au * math.sin(ra.radians)
    print(x)
    print(y)

    r = distance.au * math.cos(dec.radians)
    z = distance.au * math.sin(dec.radians)
    #print(x)
    print(z)

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
    print(x)
    print(y)
    print(z)
    print(c)
    return x, y, z, r, c

def figmap(fig):
    plt.cla()
    ax = fig.add_subplot(111, projection='3d')
    ax.legend()
    hosei = 3.0
    ax.set_xlim(-1.0 * hosei, hosei)
    ax.set_ylim(-1.0 * hosei, hosei)
    ax.set_zlim(-1.0 * hosei, hosei)
    x, y, z, r, c = createMap()
    ite = ax.scatter(x, y, z, c=c)
    i = 0
    for rr in r:
        q=Circle((0, 0), rr, ec=c[i], fill=False)
        ax.add_patch(q)
        art3d.pathpatch_2d_to_3d(q, z=0, zdir="z")
        i += 1
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    return ite

fig = plt.figure(figsize=(10,10))
figmap(fig)
#ani = animation.FuncAnimation(fig, figmap, fargs=('a'), interval=300, blit=True)
plt.show()
