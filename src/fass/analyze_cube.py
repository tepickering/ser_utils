import numpy as np

import matplotlib.pyplot as plt

import astropy.units as u
from astropy import stats, visualization

import photutils


def moments(data, aperture_diameter=76.2 * u.mm, wavelength=0.5 * u.um, pixel_scale=0.93 * u.arcsec):
    """
    Returns (height, x, y, width_x, width_y)
    the gaussian parameters of a 2D distribution by calculating its
    moments

    Arguments
    ---------
    data : 2D ~numpy.ndarray
        2D image to analyze
    aperture_diameter : ~astropy.units.Quantity (default: 76.2 mm)
        Diameter of aperture used to obtain image
    wavelength : ~astropy.units.Quantity (default: 0.5 um)
        Wavelength of the observation
    pixel_scale : ~astropy.units.Quantity (default: 0.93 arcsec/pixel)
        Angle subtended by each pixel

    Returns
    -------
    (height, x, y, width_x, width_y) : tuple of floats
        Peak flux, X centroid, Y centroid, X sigma, Y sigma
    """
    total = data.sum()
    dx = pixel_scale.to(u.radian).value  # convert pixel scale to radians
    X, Y = np.indices(data.shape)
    x = (X * data).sum() / total
    y = (Y * data).sum() / total
    col = data[:, int(y)]
    width_x = np.sqrt(
        abs((np.arange(col.size) - y) ** 2 * col).sum() / col.sum()
        )
    row = data[int(x), :]
    width_y = np.sqrt(
        abs((np.arange(row.size) - x) ** 2 * row).sum() / row.sum()
        )
    height = data.max()
    strehl = (height / total) * (4.0 / np.pi) * (wavelength / (aperture_diameter * dx)).decompose().value ** 2
    return height, strehl, x, y, width_x, width_y


def seeing(
    sigma,
    baseline=143 * u.mm,
    aperture_diameter=76.2 * u.mm,
    wavelength=0.5 * u.um,
    pixel_scale=0.93 * u.arcsec,
    direction='longitudinal'):
    """
    Calculate seeing from image motion variance, sigma, using the equations from
    Tokovinin (2002; https://www.jstor.org/stable/10.1086/342683). Numbers are for the
    MMTO's 3-aperture Hartmann mask on an LX200 with an ASI 432MM camera (9 um pixels).
    For this system, 1.22 * lambda/D is 1.66 arcsec (1.78 pixels)

    Arguments
    ---------
    sigma : float
        Standard deviation of differential image motion in pixels
    baseline : ~astropy.units.Quantity (default: 143 mm)
        Distance between aperture centers
    aperture_diameter : ~astropy.units.Quantity (default 76.2 mm)
        Diameter of DIMM apertures
    wavelength : ~astropy.units.Quantity (default: 0.5 um)
        Effective wavelength of observation
    pixel_scale : ~astropy.units.Quantity (default: 0.93 arcsec/pixel)
        Angle subtended by each pixel
    """
    b = (baseline / aperture_diameter).decompose().value
    variance = sigma * (pixel_scale.to(u.radian).value) ** 2.0
    k = {}
    k['longitudinal'] = 0.364 * (1.0 - 0.532 * b ** (-1.0 / 3.0) - 0.024 * b ** (-7.0 / 3.0))
    k['transverse'] = 0.364 * (1.0 - 0.798 * b ** (-1.0 / 3.0) + 0.018 * b ** (-7.0 / 3.0))

    if direction not in k:
        raise ValueError(f"Valid motion directions are {' and '.join(k.keys())}")

    seeing = 0.98 * ((aperture_diameter / wavelength).decompose().value ** 0.2) * ((variance / k[direction]) ** 0.6) * u.radian
    return seeing.to(u.arcsec)


def find_apertures(data, fwhm=7.0, threshold=7.0, plot=False, ap_size=5, contrast=0.05, std=None):
    """
    Use photutils.DAOStarFinder() to find and centroid star images from each DIIMM aperture.

    Parameters
    ----------
    data : FITS filename or 2D ~numpy.ndarray
        Reference image to determine aperture positions
    fwhm : float (default: 7.0)
        FWHM in pixels of DAOfind convolution kernel
    threshold : float (default: 5.0)
        DAOfind threshold in units of the standard deviation of the image
    plot: bool (default: False)
        Toggle plotting of the reference image and overlayed apertures
    ap_radius : float (default: 5)
        Radius of plotted apertures in pixels
    contrast : float (default: 0.05)
        ZScale contrast factor
    std : float or None (default: None)
        Standard deviation of image statistics, calculate if None
    """
    if std is None:
        mean, median, std = stats.sigma_clipped_stats(data, sigma=3.0, maxiters=5)

    daofind = photutils.DAOStarFinder(fwhm=fwhm, threshold=threshold*std, sharphi=0.95, brightest=3)
    stars = daofind(data)

    if stars is None:
        raise Exception("No stars detected in image")

    positions = list(zip(stars['xcentroid'], stars['ycentroid']))
    apertures = photutils.CircularAperture(positions, r=ap_size)

    fig = None
    if plot:
        fig, ax = plt.subplots()
        fig.set_label("DIMM Apertures")
        im, _ = visualization.imshow_norm(
            data,
            ax,
            origin='lower',
            interval=visualization.ZScaleInterval(contrast=contrast),
            stretch=visualization.LinearStretch()
        )
        fig.colorbar(im)
        apertures.plot(color='red', lw=1.5, alpha=0.5, axes=ax)
    return apertures, fig