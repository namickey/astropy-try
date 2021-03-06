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
    #ret.append(sincos(planets, 'sun', 'mercury', t))
    ret.append(sincos(planets, 'sun', 'venus', t))
    ret.append(sincos(planets, 'sun', 'earth', t))
    ret.append(sincos(planets, 'sun', 'mars', t))
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

'''
秒速10km = 日速  864,000km
秒速20km = 日速1,728,000km
秒速30km = 日速2,592,000km

秒速10km = 地球直径を12,756.2kmを21.3分で通過する
秒速20km = 地球直径を12,756.2kmを10.6分で通過する
秒速30km = 地球直径を12,756.2kmを7.1分で通過する

秒速10km = 太陽直径を1,392,000kmを38.7時間で通過する
秒速20km = 太陽直径を1,392,000kmを19.3時間で通過する
秒速30km = 太陽直径を1,392,000kmを12.9時間で通過する

秒速10km = 太陽と地球間を149,000,000.0kmを172.5日で通過する
秒速20km = 太陽と地球間を149,000,000.0kmを86.2日で通過する
秒速30km = 太陽と地球間を149,000,000.0kmを57.5日で通過する

秒速10km = 太陽と木星間を778,300,000.0kmを900.8日で通過する
秒速20km = 太陽と木星間を778,300,000.0kmを450.4日で通過する
秒速30km = 太陽と木星間を778,300,000.0kmを300.3日で通過する
'''

def initSates():
    sate_size = 30
    sates = np.zeros(sate_size, dtype=[('position', float, 3),# 人工衛星 座標 [km]
                                       ('speed',    float, 3),# 人工衛星 速度 日速
                                       ('frame_number', int, 1)])
    for i in range(sate_size):
        if i < sate_size/2:
            sates['position'][i] = [1.0, 0.0, 0.0]
            sates['speed'][i] = [0.0+0.5*i, 26.734+0.5*i, 10.0]
            sates['frame_number'][i] = 0
        else:
            sates['position'][i] = [1.0, 0.0, 0.0]
            sates['speed'][i] = [0.0+0.5*(i-sate_size/2), 26.734+0.5*(i-sate_size/2), 10.0]
            sates['frame_number'][i] = 180
    sates['position'] = sates['position']*1.496*10**8
    sates['speed'] = sates['speed']*60*60*24
    return sates

sates = initSates()

def fm(xs, rs):
    GM = 3.9859*(10**14)*60*60*24*27.0 #太陽
    return -GM*(xs/rs**3)

def moveOnGravity(sate):
    xs = sate['position'][0]
    ys = sate['position'][1]
    zs = sate['position'][2]
    dx = sate['speed'][0]
    dy = sate['speed'][1]
    dz = sate['speed'][2]
    rs = np.sqrt(xs**2 + ys**2 + zs**2)
    dx = dx + fm(xs, rs)
    dy = dy + fm(ys, rs)
    dz = dz + fm(zs, rs)
    xs = xs + dx
    ys = ys + dy
    zs = zs + dz
    return ([xs, ys, zs], [dx, dy, dz], sate['frame_number'])

fig = plt.figure(figsize=(14, 14))
ax = fig.add_subplot(111, projection='3d')
#ax.legend()
hosei = 2.5
ax.set_xlim(-1.0 * hosei, hosei)
ax.set_ylim(-1.0 * hosei, hosei)
ax.set_zlim(-1.0 * hosei, hosei)
ts = load.timescale()
t = ts.now()
x, y, z, r, c = createMap(t)
scat = ax.scatter(x, y, z, c=c)
scat.set_sizes([50]*len(x))
scat_sates = []
for i in range(len(sates)):
    sates[i] = moveOnGravity(sates[i])
    if i < len(sates)/2:
        scat_sates.append(ax.scatter(sates['position'][i][0]/(1.496*10**8),
                                     sates['position'][i][1]/(1.496*10**8),
                                     sates['position'][i][2]/(1.496*10**8), c='red'))
    else:
        scat_sates.append(ax.scatter(0, 0, 0, c='red'))

lined = createCircleData(len(x))
for h, line in enumerate(lined):
    ax.plot(line[0], line[1], line[2], c=c[h])

max_s = 0.0
min_s = 3.0

def showLength(sate, x, y, z):
    global max_s
    global min_s
    leng = np.sqrt((sate[0]-x[2])**2 + (sate[1]-y[2])**2 + (sate[2]-z[2])**2)
    if max_s < leng:
        max_s = leng
        print('max: ' + str(max_s))
    if min_s > leng:
        min_s = leng
        print('min: ' + str(min_s))

def update(frame_number):
    global scat
    scat.remove()
    print(frame_number)
    for scat_sate in scat_sates:
        scat_sate.remove()
    ts = load.timescale()
    t = ts.tt_jd(ts.now().tt+frame_number)
    x, y, z, r, c = createMap(t)
    scat = ax.scatter(x, y, z, c=c)
    scat.set_sizes([60]*len(x))
    for i in range(len(sates)):
        if sates[i]['frame_number'] <= frame_number:
            sates[i] = moveOnGravity(sates[i])
            scat_sates[i] = ax.scatter(sates['position'][i][0]/(1.496*10**8),
                                       sates['position'][i][1]/(1.496*10**8),
                                       sates['position'][i][2]/(1.496*10**8), c='red')
        else:
            scat_sates[i] = ax.scatter(0, 0, 0, c='red')
    showLength(sates['position'][0], x, y, z)

animation = FuncAnimation(fig, update, interval=30)
plt.show()
