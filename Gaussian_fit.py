#%%
import os
import numpy as np
from scipy import signal, optimize
from skimage import io
import matplotlib.pyplot as plt
#%%
path = r'C:\Users\lxiaoyang\Desktop'
os.chdir(path)
fn = 'test-1.tif'
img = io.imread(fn)
#ref = img[1,:,:]
#io.imshow(ref)

#%%
# Define a 2D Gaussian function
def gaussian_2d(xy, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x, y = xy
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))
    return g.ravel()

#%%
path = r'C:\Users\lxiaoyang\Desktop'
os.chdir(path)
fn = 'test-1.tif'
img = io.imread(fn)
beam_x_list = []
beam_y_list = []
sigma_x_list = []
sigma_y_list = []
ini_x = img.shape[2]//2 #initial guess for beam position x
ini_y = img.shape[1]//2 #initial guess for beam position y
for z in range(img.shape[0]):
    ref = img[z,:,:]
    # Create x and y indices
    x = np.linspace(0, ref.shape[1] - 1, ref.shape[1])
    y = np.linspace(0, ref.shape[0] - 1, ref.shape[0])
    x, y = np.meshgrid(x, y)

    # Initial guess for the parameters
    initial_guess = (np.max(ref), ini_x, ini_y, 10, 10, 0, 10)
    # Bounds for the parameters
    bounds = (
        [0, 0, 0, 0, 0, -np.pi/4, 0],  # Lower bounds
        [np.inf, ref.shape[1], ref.shape[0], np.inf, np.inf, np.pi/4, np.max(ref)]  # Upper bounds
    )

    # Fit the Gaussian model to the data
    popt, _ = optimize.curve_fit(gaussian_2d, (x, y), ref.ravel(), p0=initial_guess,bounds=bounds,maxfev=10000)

    # Extract the beam position from the fit parameters
    beam_x = popt[1]
    beam_y = popt[2]
    sigma_x = popt[3]
    sigma_y = popt[4]

    print(f"Slice: {z}, Beam position: x = {beam_x}, y = {beam_y}, sigma_x = {sigma_x}, sigma_y = {sigma_y}")
    beam_x_list.append(beam_x)
    beam_y_list.append(beam_y)
    sigma_x_list.append(float(sigma_x))
    sigma_y_list.append(float(sigma_y))
    ini_x = beam_x #update initial guess for beam position x
    ini_y = beam_y #update initial guess for beam position y
    # Use the optimized parameters to create the fitted Gaussian
    data_fitted = gaussian_2d((x, y), *popt)

    # Plot the results
    fig, ax = plt.subplots(1, 1)
    ax.imshow(ref, cmap=plt.cm.jet, origin='lower', extent=(x.min(), x.max(), y.min(), y.max()))
    ax.contour(x, y, data_fitted.reshape(ref.shape[0], ref.shape[1]), 8, colors='w')
    plt.show()

# %%
#shift image
from scipy.ndimage import shift
fn = 'test-1.tif'
img = io.imread(fn)
ref = img[0,:,:]
mv_y = []
mv_x = []
for i, y in enumerate(beam_y_list):
    if i == 0:
        ref_y = y
        ref_x = beam_x_list[i]
    else:
        y_mv = ref_y - y
        x_mv = ref_x - beam_x_list[i]
        mv_y.append(y_mv)
        mv_x.append(x_mv)
for i,y2 in enumerate(mv_y):
    img[i+1,:,:] = shift(img[i+1,:,:], (y2, mv_x[i]))
# %%
#save image
io.imsave('test-1_shifted.tif',img)