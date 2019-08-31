from astropy.coordinates import SkyCoord
import astropy.units as u


NCP = SkyCoord(ra=0, dec=90, unit=u.deg)
SCP = SkyCoord(ra=0, dec=-90, unit=u.deg)

class SkyArea:
    def __init__(self, ra0, ra1, dec0, dec1, mag_min):
        self.ra_min  = min(ra0, ra1)
        self.ra_max  = max(ra0, ra1)
        self.dec_min = min(dec0, dec1)
        self.dec_max = max(dec0, dec1)
        self.mag_min = mag_min

    def centered(ra, dec, radius, mag_min):
        sky_coord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
        if sky_coord.separation(NCP) < radius * u.deg or sky_coord.separation(SCP) < radius * u.deg:
            ra_min = 0
            ra_max = 24
        else:
            right_ascensions = [sky_coord.directional_offset_by(angle * u.deg, radius* u.deg).ra.hourangle for angle in [0, 90, 180, 270, 360]]
            ra_min = min(right_ascensions)
            ra_max = max(right_ascensions)

        dec_min = max(dec - radius, -90)
        dec_max = min(dec + radius, 90)
        return SkyArea(ra_min, ra_max, dec_min, dec_max, mag_min)

    def __str__(self):
        return 'SkyArea: ra_min={}, ra_max={}, dec_min={}, dec_max={}, mag_min={}'.format(self.ra_min, self.ra_max, self.dec_min, self.dec_max, self.mag_min)

    def __repr__(self):
        return self.__str__()

SKY_AREA_ORION  = SkyArea(4.5, 6.5, -15, 15, 8)
SKY_AREA_TAURUS = SkyArea(4, 6, 10, 30, 8)
SKY_AREA_NORTH = SkyArea(0, 24, 50, 90, 7)
SKY_AREA_SOUTH = SkyArea(0, 24, -50, -90, 7)
SKY_AREA_URSA_MINOR = SkyArea(14, 18, 60, 90, 9)
