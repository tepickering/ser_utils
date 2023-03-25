from pathlib import Path

from functools import partial
from multiprocessing import Pool

import numpy as np

from skimage.transform import warp_polar

import matplotlib.pyplot as plt

import astropy.units as u
from astropy import stats, visualization

import photutils

from fass.ser import load_ser_file


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
    Y, X = np.indices(data.shape)
    x = (X * data).sum() / total
    y = (Y * data).sum() / total
    col = data[:, int(x)]
    width_x = np.sqrt(
        abs((np.arange(col.size) - y) ** 2 * col).sum() / col.sum()
    )
    row = data[int(y), :]
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
    direction='longitudinal'
):
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
        Angle subtended by each pixel (default is for 9 um pixels and 2000 mm focal length)
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


def find_apertures(data, fwhm=7.0, threshold=7.0, plot=False, ap_size=5, contrast=0.05, brightest=3, std=None):
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

    daofind = photutils.DAOStarFinder(fwhm=fwhm, threshold=threshold*std, sharphi=0.95, brightest=brightest)
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


def dimm_calc(data, aps):
    """
    Calculate longitudinal distance for each baseline in the 3-aperture Hartmann-DIMM mask

    Arguments
    ---------
    data : 2D numpy.ndarray image
        Image frame to perform centroids on

    aps : ~photutils.CircularAperture
        Aperture positions
    """
    ap_stats = photutils.ApertureStats(data, aps)
    ap_pos = ap_stats.centroid
    new_aps = photutils.CircularAperture(ap_pos, aps.r)
    base1 = ap_pos[1] - ap_pos[0]
    base2 = ap_pos[2] - ap_pos[0]
    base3 = ap_pos[2] - ap_pos[1]
    d_base1 = np.sqrt(np.dot(base1.T, base1))
    d_base2 = np.sqrt(np.dot(base2.T, base2))
    d_base3 = np.sqrt(np.dot(base3.T, base3))

    return new_aps, [d_base1, d_base2, d_base3]


def analyze_dimm_cube(filename, init_ave=3, plot=False):
    """
    Analyze an SER format data cube of DIMM observations and calculate the seeing from the
    differential motion along the longitudinal axis of each baseline. This is currently hard-coded
    to the 3-aperture mask used at the MMTO.

    Arguments
    ---------
    filename : str or ~pathlib.Path
        Filename of the SER data cube to analyze
    init_ave : int
        Number of frames at the beginning of the cube to average to do initial aperture location
    """
    cube = load_ser_file(Path(filename))

    nframes = cube['data'].shape[0]

    apertures, fig = find_apertures(cube['data'][0:init_ave, :, :].sum(axis=0), plot=plot)

    baselines = []
    positions = []

    for i in range(nframes):
        apertures, ap_distances = dimm_calc(cube['data'][i, :, :], apertures)
        baselines.append(ap_distances)
        positions.append(apertures.positions.mean(axis=0))

    baselines = np.array(baselines).transpose()
    positions = np.array(positions).transpose()

    seeing_vals = []
    for baseline in baselines:
        seeing_vals.append(seeing(baseline.std()))

    ave_seeing = u.Quantity(seeing_vals).mean()

    return ave_seeing, seeing_vals, baselines, positions, cube['frame_times'], fig


def process_fass_image(image, background_box_size=15, width_cut=0.1):
    """
    Process FASS image to measure background, image statistics, pupil center, and pupil width

    Parameters
    ----------
    image : np.ndarray
        Raw image to process
    background_box_size : int (default: 15)
        Size of the box to use for background estimation. Uses the four corners of the image.
    width_cut : float (default: 0.1)
        Fraction of the maximum pixel value to use for determining the width of the pupil.

    Returns
    -------
    proc_image : np.ndarray
        Background subtracted image
    bkg_mean : float
        Mean background value
    bkg_median : float
        Median background value
    bkg_std : float
        Standard deviation in the background regions
    x : float
        X coordinate of the pupil center
    y : float
        Y coordinate of the pupil center
    width : float
        Width of the pupil
    """
    ul = image[:background_box_size, :background_box_size]
    ll = image[-background_box_size:, :background_box_size]
    ur = image[:background_box_size, -background_box_size:]
    lr = image[-background_box_size:, -background_box_size:]
    background = np.vstack([ul, ll, ur, lr])
    bkg_mean = np.mean(background)
    bkg_median = np.median(background)
    bkg_std = np.std(background)
    proc_image = image.copy() - bkg_median

    Y, X = np.indices(proc_image.shape)
    proc_sum = proc_image.sum()
    x = (X * proc_image).sum() / proc_sum
    y = (Y * proc_image).sum() / proc_sum

    x_sum = proc_image.sum(axis=0)
    y_sum = proc_image.sum(axis=1)

    width_x = np.where(x_sum > width_cut * x_sum.max())[0].size
    width_y = np.where(y_sum > width_cut * y_sum.max())[0].size

    width = (width_x + width_y) / 2
    return proc_image, bkg_mean, bkg_median, bkg_std, x, y, width


def init_fass_cube(image_cube, n_frames=500):
    """
    Average first n_frames of the image cube to determine the pupil size and initial pupil center position.

    Parameters
    ----------
    image_cube : np.ndarray
        Image cube to process
    n_frames : int (default: 500)
        Number of frames to average

    Returns
    -------
    proc_image : np.ndarray
        Background subtracted, coadded first n_frames of image_cube
    x : float
        X coordinate of the pupil center
    y : float
        Y coordinate of the pupil center
    width : float
        Width of the pupil
    """
    image = image_cube[:n_frames, :, :].mean(axis=0)
    proc_image, _, _, _, x, y, width = process_fass_image(image)
    return proc_image, x, y, width


def _process_slice_func(image, x0=0, y0=0, radius=100, output_shape=(100, 100), center_gain=0.1):
    proc_image, _, _, _, x, y, _ = process_fass_image(image)
    x0 = x0 + center_gain * (x - x0)
    y0 = y0 + center_gain * (y - y0)
    unwrapped = warp_polar(
        proc_image,
        output_shape=output_shape,
        center=(x0, y0),
        radius=radius,
        scaling='linear',
        preserve_range=True
    )
    return unwrapped


def unwrap_fass_cube(image_cube, center_gain=0.1, radial_pad=10, oversample=2, nproc=8):
    """
    Unwrap FASS image cube to polar coordinates.

    Parameters
    ----------
    image_cube : np.ndarray
        Image cube to unwrap
    center_gain : float (default: 0.1)
        Gain factor to use for centering the pupil
    radial_pad : int (default: 20)
        Number of pixels to pad the radial dimension
    oversample : int (default: 2)
        Oversampling factor to use for the unwrapping
    nproc : int (default: 8)
        Number of processes to use for parallel processing

    Returns
    -------
    unwrapped_cube : np.ndarray
        Unwrapped image cube
    """
    _, x, y, width = init_fass_cube(image_cube)
    x0 = x
    y0 = y
    radius = width/2 + radial_pad
    unwrapped_cube = []
    output_shape = (int(2 * np.pi * oversample * radius), int(oversample * radius))
    with Pool(processes=nproc) as pool:
        proc_slice = partial(_process_slice_func, x0=x0, y0=y0, radius=radius, output_shape=output_shape, center_gain=center_gain)
        unwrapped_cube = pool.map(proc_slice, image_cube)
    return np.stack(unwrapped_cube)
