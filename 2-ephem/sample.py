# coding:utf-8
import ephem
import datetime

osaka = ephem.city('Tokyo')
osaka.date = datetime.datetime.utcnow()
sun = ephem.Sun()
print(ephem.localtime(osaka.next_rising(sun)))
