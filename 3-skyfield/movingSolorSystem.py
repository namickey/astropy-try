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

def createCircleData():
    lineData=[]
    for i in range(5):
        lineData.append([[],[],[]])
    for i in range(690):
        ts = load.timescale()
        t = ts.tt_jd(ts.now().tt+i)
        x, y, z, r, c = createMap(t)
        [lineData[h][0].append(d) for h, d in enumerate(x)]
        [lineData[h][1].append(d) for h, d in enumerate(y)]
        [lineData[h][2].append(d) for h, d in enumerate(z)]
    return lineData

# 刻み幅
h = 0.015625  # [day]
# 万有引力定数×惑星の質量(E：地球，M：月)
GE = 2.975537 * 10**15  * 27  # [km^3*day^-2]
GM = 3.659916 * 10**13   # [km^3*day^-2]
# 人工衛星
xs = 1.496*10**8*0.5 # [km]
ys = 1.496*10**8*0.5
dxs_dt = 1.28 * 60 * 60 * 24  # [km/day]
# -6.17[km/s] を -6.17[km/day]に変換
dys_dt = 6.28 * 60 * 60 * 24

# 月
R = 384400  # [km]
theta = 2.435  # [rad]
dtheta_dt = 0.2302823  # [day^-1]

xm = R * np.cos(theta)
ym = R * np.sin(theta)
dxm_dt = -dtheta_dt * R * np.sin(theta)
dym_dt =  dtheta_dt * R * np.cos(theta)

# 人工衛星の軌道の二階微分方程式(xs, ys で同じ)
def fs(xs, xm, rs, rm, rms):
    return -GE*(xs/rs**3) + GM*((xm - xs)/rms**3 - xm/rm**3)

# 月の軌道の二階微分方程式(xs, ys で同じ)
def fm(xm, rm):
    return -GE*(xm/rm**3)

def moveOnGravity():
    global xs
    global ys
    global xm
    global ym
    global dxm_dt
    global dym_dt
    global dxs_dt
    global dys_dt
    # １次
    rs  = np.sqrt(xs**2 + ys**2)
    rm  = np.sqrt(xm**2 + ym**2)
    rms = np.sqrt((xm - xs)**2 + (ym - ys)**2)

    fs_x1 = fs(xs, xm, rs, rm, rms)
    fs_y1 = fs(ys, ym, rs, rm, rms)
    fm_x1 = fm(xm, rm)
    fm_y1 = fm(ym, rm)

    xs_1 = xs + 2/5*h*dxs_dt + 2/25 * h**2 * fs_x1
    ys_1 = ys + 2/5*h*dys_dt + 2/25 * h**2 * fs_y1
    xm_1 = xm + 2/5*h*dxm_dt + 2/25 * h**2 * fm_x1
    ym_1 = ym + 2/5*h*dym_dt + 2/25 * h**2 * fm_y1

    # ２次
    rs  = np.sqrt(xs_1**2 + ys_1**2)
    rm  = np.sqrt(xm_1**2 + ym_1**2)
    rms = np.sqrt((xm_1 - xs_1)**2 + (ym_1 - ys_1)**2)

    fs_x2 = fs(xs_1, xm_1, rs, rm, rms)
    fs_y2 = fs(ys_1, ym_1, rs, rm, rms)
    fm_x2 = fm(xm_1, rm)
    fm_y2 = fm(ym_1, rm)

    xs_2 = xs + 2/3*h*dxs_dt + 2/9 * h**2 * fs_x1
    ys_2 = ys + 2/3*h*dys_dt + 2/9 * h**2 * fs_y1
    xm_2 = xm + 2/3*h*dxm_dt + 2/9 * h**2 * fm_x1
    ym_2 = ym + 2/3*h*dym_dt + 2/9 * h**2 * fm_y1

    # ３次
    rs  = np.sqrt(xs_2**2 + ys_2**2)
    rm  = np.sqrt(xm_2**2 + ym_2**2)
    rms = np.sqrt((xm_2 - xs_2)**2 + (ym_2 - ys_2)**2)

    fs_x3 = fs(xs_2, xm_2, rs, rm, rms)
    fs_y3 = fs(ys_2, ym_2, rs, rm, rms)
    fm_x3 = fm(xm_2, rm)
    fm_y3 = fm(ym_2, rm)

    xs_3 = xs + 4/5*h*dxs_dt + 4/25 * h**2 * (fs_x1 + fs_x2)
    ys_3 = ys + 4/5*h*dys_dt + 4/25 * h**2 * (fs_y1 + fs_y2)
    xm_3 = xm + 4/5*h*dxm_dt + 4/25 * h**2 * (fm_x1 + fm_x2)
    ym_3 = ym + 4/5*h*dym_dt + 4/25 * h**2 * (fm_y1 + fm_y2)

    # ４次
    rs  = np.sqrt(xs_3**2 + ys_3**2)
    rm  = np.sqrt(xm_3**2 + ym_3**2)
    rms = np.sqrt((xm_3 - xs_3)**2 + (ym_3 - ys_3)**2)

    fs_x4 = fs(xs_3, xm_3, rs, rm, rms)
    fs_y4 = fs(ys_3, ym_3, rs, rm, rms)
    fm_x4 = fm(xm_3, rm)
    fm_y4 = fm(ym_3, rm)


    # 結果
    xs += h * (dxs_dt + (h/192)*(23*fs_x1 + 75*fs_x2 - 27*fs_x3 + 25*fs_x4))
    ys += h * (dys_dt + (h/192)*(23*fs_y1 + 75*fs_y2 - 27*fs_y3 + 25*fs_y4))
    xm += h * (dxm_dt + (h/192)*(23*fm_x1 + 75*fm_x2 - 27*fm_x3 + 25*fm_x4))
    ym += h * (dym_dt + (h/192)*(23*fm_y1 + 75*fm_y2 - 27*fm_y3 + 25*fm_y4))

    dxs_dt += h/192 * (23*fs_x1 + 125*fs_x2 - 81*fs_x3 + 125*fs_x4)
    dys_dt += h/192 * (23*fs_y1 + 125*fs_y2 - 81*fs_y3 + 125*fs_y4)
    dxm_dt += h/192 * (23*fm_x1 + 125*fm_x2 - 81*fm_x3 + 125*fm_x4)
    dym_dt += h/192 * (23*fm_y1 + 125*fm_y2 - 81*fm_y3 + 125*fm_y4)
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
lined = createCircleData()
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

animation = FuncAnimation(fig, update, interval=2000)
plt.show()
