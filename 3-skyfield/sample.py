#coding: utf-8
import math
from skyfield.api import load
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def sincos(p1, p2):
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

    #x = distance.au * math.cos(dec.radians)
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
    return [x, y, z]

planets = load('de421.bsp')
print(planets)
ret = [[0.0, 0.0, 0.0]]
ret.append(sincos('sun', 'mercury'))
ret.append(sincos('sun', 'venus'))
ret.append(sincos('sun', 'earth'))
ret.append(sincos('sun', 'mars'))
ret.append(sincos('sun', 'JUPITER BARYCENTER'))
ret.append(sincos('sun', 'SATURN BARYCENTER'))
#ret.append(sincos('sun', 'URANUS BARYCENTER'))
#ret.append(sincos('sun', 'NEPTUNE BARYCENTER'))
x = [x[0] for x in ret]
y = [x[1] for x in ret]
z = [x[2] for x in ret]
print(x)
print(y)
print(z)
hosei = 10.0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, c=['red', 'blue', 'yellow', 'cyan', 'magenta', 'green', 'green'])
ax.legend()
ax.set_xlim(-1.0 * hosei, hosei)
ax.set_ylim(-1.0 * hosei, hosei)
ax.set_zlim(-1.0 * hosei, hosei)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
