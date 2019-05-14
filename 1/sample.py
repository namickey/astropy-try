import numpy as np
import matplotlib.pyplot as plt
from astroquery.skyview import SkyView
from astropy import units as u
from astropy.visualization import ZScaleInterval,ImageNormalize
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans
from astropy.wcs import WCS
#SkyView.list_surveys()

survey = ['2MASS-K','2MASS-H','2MASS-J']
for m in [17,43,51,78,83,104,109]:
    hdu = SkyView.get_images('M%d'%m,survey=survey,radius=20*u.arcmin,pixels=1280)
    plt.figure(figsize=[6,6]).gca(projection=WCS(hdu[0][0].header),title='M%d'%m)
    plt.imshow(np.stack([ImageNormalize(hdu[i][0].data,interval=ZScaleInterval())(hdu[i][0].data) for i in range(3)],2))
    plt.savefig('2mass_M%d.jpg'%m)
    plt.show()

position = "M8"
survey = ['AKARI N60', 'AKARI WIDE-S', 'AKARI WIDE-L', 'AKARI N160']
radius = 5*u.deg
pixels = 800
hdu = SkyView.get_images(position=position, survey=survey, radius=radius, pixels=pixels)

plt.figure(figsize=[7, 7])
for i in range(4):
    plt.subplot(221+i, title=survey[i])
    plt.imshow(hdu[i][0].data, origin='lower', cmap='hot')
plt.show()
