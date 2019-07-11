#coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from skyfield.api import load
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d

#重力プログラミング入門「第1回：地球の重力下で人工衛星を公転軌道に乗せる」
#https://www.slideshare.net/piacere_ex/fukuoka1

def sincos(planets, p1, p2, t):
    pla1, pla2 = planets[p1], planets[p2]
    astrometric = pla1.at(t).observe(pla2)
    ra, dec, distance = astrometric.radec()
    x = distance.au * math.cos(ra.radians)
    y = distance.au * math.sin(ra.radians)
    r = distance.au * math.cos(dec.radians)
    z = distance.au * math.sin(dec.radians)
    #print('赤経 (right ascension, RA) :' + str(ra))
    #print('赤経：天体と春分点との角度の隔たりを東方向を正にとって表す。 ')
    #print(dec.radians)
    #print('赤緯 (declination, Dec) ：' + str(dec))
    #print('赤緯：天体と天の赤道の間の角度の隔たりを表す')
    #print(distance)
    return [x, y, z, r]

def createMap(t):
    planets = load('de421.bsp')
    ret = [[0.0, 0.0, 0.0, 0.0]]
    ret.append(sincos(planets, 'sun', 'mercury', t))
    ret.append(sincos(planets, 'sun', 'venus', t))
    #ret.append(sincos(planets, 'sun', 'earth', t))
    #ret.append(sincos(planets, 'sun', 'mars', t))
    #ret.append(sincos(planets, 'sun', 'JUPITER BARYCENTER', t))
    #ret.append(sincos(planets, 'sun', 'SATURN BARYCENTER', t))
    #ret.append(sincos(planets, 'sun', 'URANUS BARYCENTER', t))
    #ret.append(sincos(planets, 'sun', 'NEPTUNE BARYCENTER', t))
    x = [x[0] for x in ret]
    y = [x[1] for x in ret]
    z = [x[2] for x in ret]
    r = [x[3] for x in ret]
    c = ['red', 'blue', 'yellow', 'cyan', 'magenta', 'green', 'brown']
    c = c[:len(x)]
    return x, y, z, r, c

def createCircleData(s):
    lineData=[]
    for i in range(s):
        lineData.append([[],[],[]])
    for i in range(690):
        ts = load.timescale()
        t = ts.tt_jd(ts.now().tt+i)
        x, y, z, r, c = createMap(t)
        [lineData[h][0].append(d) for h, d in enumerate(x)]
        [lineData[h][1].append(d) for h, d in enumerate(y)]
        [lineData[h][2].append(d) for h, d in enumerate(z)]
    return lineData

# 万有引力定数×惑星の質量(E：地球，M：月)
GE = 2.975537 * 10**15  * 27  # [km^3*day^-2]
GM = 3.659916 * 10**13   # [km^3*day^-2]
G = 1.267*10**8*27.0
# 人工衛星
xs = 1.496*10**8*0.1 # [km]
ys = 1.496*10**8*0.1
dx = 100.0
dy = 0.0
def fm(xm, rm):
    return -G*(xm/rm**3)

def moveOnGravity():
    global xs
    global ys
    global dx
    global dy
    rs  = np.sqrt(xs**2 + ys**2)
    dx = dx + fm(xs, rs)
    dy = dy + fm(ys, rs)
    xs += dx
    ys += dy
    return ((xs/(1.496*10**8)), (ys/(1.496*10**8)), (0.0))

fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(111, projection='3d')
#ax.legend()
hosei = 1.3
ax.set_xlim(-1.0 * hosei, hosei)
ax.set_ylim(-1.0 * hosei, hosei)
ax.set_zlim(-1.0 * hosei, hosei)
ts = load.timescale()
t = ts.now()
x, y, z, r, c = createMap(t)
scat = ax.scatter(x, y, z, c=c)
scat.set_sizes([50]*len(x))
sate = moveOnGravity()
scat_sate = ax.scatter(sate[0], sate[1], sate[2], c='red')
lined = createCircleData(len(x))
for h, line in enumerate(lined):
    ax.plot(line[0], line[1], line[2], c=c[h])

def update(frame_number):
    global scat
    global scat_sate
    scat.remove()
    scat_sate.remove()
    ts = load.timescale()
    t = ts.tt_jd(ts.now().tt+frame_number)
    x, y, z, r, c = createMap(t)
    scat = ax.scatter(x, y, z, c=c)
    scat.set_sizes([60]*len(x))
    sate = moveOnGravity()
    print(sate)
    scat_sate = ax.scatter(sate[0], sate[1], sate[2], c='red')

animation = FuncAnimation(fig, update, interval=80)
plt.show()
