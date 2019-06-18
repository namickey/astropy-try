#coding: utf-8

from skyfield.api import load

planets = load('de421.bsp')
earth, mars = planets['earth'], planets['mars']
ts = load.timescale()
t = ts.now()
astrometric = earth.at(t).observe(mars)
ra, dec, distance = astrometric.radec()

print('赤経 (right ascension, RA) :' + str(ra))
print('赤経：天体と春分点との角度の隔たりを東方向を正にとって表す。 ')
print('')
print('赤緯 (declination, Dec) ：' + str(dec))
print('赤緯：天体と天の赤道の間の角度の隔たりを表す')
print('')
print(distance)
