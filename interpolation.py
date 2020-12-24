
"""
Ordinary Kriging Example
========================

First we will create a 2D dataset together with the associated x, y grids.

"""

import numpy as np
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
import pandas as pd

# https://pykrige.readthedocs.io/en/latest/generated/pykrige.ok.OrdinaryKriging.html
# https://www.earthinversion.com/geophysics/plotting-the-geospatial-data-clipped-by-coastlines-in-python/


def interpolation():

    data_in = pd.read_csv("./data/24.csv", delimiter=',', usecols=[2, 3, 4])
    data = data_in.to_numpy()

    # print("data:    ", data)

    print("data:    ", data.shape)

    # data = np.array(
    #     [
    #         [0.3, 1.2, 0.47],
    #         [1.9, 0.6, 0.56],
    #         [1.1, 3.2, 0.74],
    #         [3.3, 4.4, 1.47],
    #         [4.7, 3.8, 1.74],
    #     ]
    # )
    #

    lons = data[:, 0]
    lats = data[:, 1]
    data = data[:, 2]

    grid_space = 0.5
    # grid_space is the desired delta/step of the output array
    grid_lon = np.arange(np.amin(lons), np.amax(lons), grid_space)
    grid_lat = np.arange(np.amin(lats), np.amax(lats), grid_space)

    # print("grid_lon:    ", grid_lon)
    # print("grid_lat:    ", grid_lat)

    ###############################################################################
    # Create the ordinary kriging object. Required inputs are the X-coordinates of
    # the data points, the Y-coordinates of the data points, and the Z-values of the
    # data points. If no variogram model is specified, defaults to a linear variogram
    # model. If no variogram model parameters are specified, then the code automatically
    # calculates the parameters by fitting the variogram model to the binned
    # experimental semivariogram. The verbose kwarg controls code talk-back, and
    # the enable_plotting kwarg controls the display of the semivariogram.

    OK = OrdinaryKriging(
        lons, lats, data,
        variogram_model="spherical",
        nlags=6,
        verbose=True,
        enable_plotting=False,
        enable_statistics=True,
        # coordinates_type="geographic",
    )

    ###############################################################################
    # Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
    # grid of points, on a masked rectangular grid of points, or with arbitrary points.
    # (See OrdinaryKriging.__doc__ for more information.)

    z, ss = OK.execute("grid", grid_lon, grid_lat)

    ###############################################################################
    # Writes the kriged grid to an ASCII grid file and plot it.

    # print("Value:    ", z.shape)
    # print("ss:    ", ss)

    # https://pykrige.readthedocs.io/en/latest/api.html#tools
    kt.write_asc_grid(grid_lon, grid_lat, z, filename="./data/ok-output.asc")

    # np.savetxt('./dataok-output.txt', z, fmt="%f", delimiter=",")

    # np.savez("./dataok-output.npz", grid_lon = grid_lon, grid_lat = grid_lat, z = z)

    # https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#scatter-plots
    #

    # plt.imshow(z)
    # plt.show()

    return z


if __name__ == '__main__':
    interpolation()
