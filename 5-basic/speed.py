#coding:utf-8

ss = 30      #秒速        30km/s
sh = ss*3600 #時速   108,000km/h  10万8千キロ
sd = sh*24   #日速 2,592,000km/d 259万2千キロ
for i in range(10,40,10):
    print('秒速{}km = 日速{:9,}km'.format(i, i*3600*24))

def rspeed(name, r):
    for i in range(10,40,10):
        if r < 7000.0:
            print('秒速{0}km = {1}{2:,}kmを{3:.1f}分で通過する'.format(i, name, r*2, r*2/i/60)) #7分で地球直径分を移動
        elif r < 700000:
            print('秒速{0}km = {1}{2:,}kmを{3:.1f}時間で通過する'.format(i, name, r*2, r*2/i/60/60))
        else:
            print('秒速{0}km = {1}{2:,}kmを{3:.1f}日で通過する'.format(i, name, r, r/i/60/60/24))

earth_r = 6378.1 #km 赤道半径
rspeed('地球直径を', earth_r)
sun_r = 696000 #km 赤道半径
rspeed('太陽直径を', sun_r)
au = 1.49*10**8
rspeed('太陽と地球間を', au)
rspeed('太陽と木星間を', 7.783*10**8)
