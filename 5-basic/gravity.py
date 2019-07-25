#coding:utf-8
import numpy as np

#地球の重さ
Me = 5.972*10**24
#万有引力定数
G = 6.67259*10**-11 # m**3/s**2/kg**1

print('G*Me:{:20}'.format(G*Me))

#地心重力定数
GMe = 3.986*10**14 # m**3/s**2
print('GMe:{:21}'.format(GMe))

#日心重力定数
GMs = 1.327*10**20 # m**3/s**2

# 「m3 →　km3」では、1000を3回掛ける。
μ = 3.986*10**14
print('μ:{:22}'.format(μ))
print('μk:{:21}'.format(μ/1000/1000/1000))
μk = 398600 #[km３/s２]
μk = 3.986*10**5 #[km３/s２]
print('μk:{:21}'.format(μk))

day = 60*60*24
au = 1.496*10**8
print('μau:{:25}'.format(μk/au/au/au))
print('μauday:{:22}'.format(μk/au/au/au*day*day))

s = 10 # km/s
print('s:{:26}km'.format(s))
print('sau:{:24}km'.format(s/au))
sday = 10*day #km/day
print('sday:{:23}km'.format(sday))
print('sdayau:{:21}au'.format(sday/au))

def fm(GMs, xs, rs):
    print(GMs)
    return -GMs*(xs/rs**3)

GMs = 1.327*10**20 # m**3/s**2
print(fm(GMs/1000/1000/1000/au/au/au*day*day, sday/au, 1))
print(fm(GMs/1000/1000/1000*day*day, sday, 1*au))
