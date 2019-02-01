import numpy as np
from scipy import signal
from skimage.util import pad
from skimage.measure import compare_ssim
from skimage.measure import compare_nrmse
from timeit import default_timer as timer


def compute_mse(im1, im2):
    """
    Calculate the Mean Square Error of Two Single Band Images.
    The two input images must be the same size and shape.
    A valid comparison will return two objects:
    1.) A Mean Square Error Value
    2.) The map (array) of element-wise square errors.
    """
    start = timer()
    print("Computing Mean Square Error...")
    mse_value = compare_nrmse(im1, im2, norm_type='Euclidean')
    square_error_map = (im1 - im2) ** 2

    end = timer()
    print("...Complete. Elapsed Time: [s] " + str((end - start))[0:4])

    return round(mse_value, 3), square_error_map


def compute_ssim(im1, im2, win_size):
    """
    Compute Structural Similarity Index of two single band images.

    The human visual system is well adapted to extracting structural
    information from a scene. Structural information refers to how
    objects are arranged in a scene independent of background
    intensity and contrast (Wang et al., 2004). "We define
    structural information in an image as those attributes that
    represent the structure of objects in the scene, independent of
    the average luminance and contrast. Since luminance and contrast
    can vary across a scene, we use the local luminance and contrast
    for our definition. Luminance, contrast, and structure
    comparisons make up SSIM. Brightness in the SSIM map indicates
    the magnitude of the local SSIM index (squared for visibility).

     Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P.
     (2004). Image quality assessment: From error visibility to
     structural similarity. IEEE Transactions on Image Processing,
     13, 600-612.
     https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf,
     DOI:10.1109/TIP.2003.819861

    Args:
        im1 (ndarray): 2d array for similarity
        im2 (ndarray): 2d array, same size/shape as im1
        width (int): window size for comparison convolution, must be
        odd (default: 3)
    Returns:
        ssim (tuple): mean value and array of SSIM values
    Raises:
        Exception: description
    """

    start = timer()
    if win_size % 2 != 1:
        print('Please provide an odd integer for the window size.')
    else:
        print("Computing Structural Similarity Index...")
        ssim = compare_ssim(im1, im2, win_size=win_size,
                            gaussian_weights=True, full=True)

        end = timer()
        print("...Complete. Elapsed Time: " + str((end - start))[0:4])

        return ssim


def cw_ssim(im1, im2, width):
    """
    Compute a complex wavelet implementation of SSIM (CW-SSIM).

    CW-SSIM insensitive to translation, scaling and rotation of
    images. A value of +1 indicates perfect similarity and a value of
    -1 indicates lack of similarity.

    Args:
        im1 (ndarray): 2d array for similarity
        im2 (ndarray): 2d array, same size/shape as im1
        width (int): wavelet width for convolution (default: 30)
    Returns:
        ssim (tuple): mean value and array of CW-SSIM values
    Raises:
        Exception: description
    """
    start = timer()
    print("Computing Complex Wavelet Structural Similarity Index...")

    # Define a width for the wavelet convolution
    widths = np.arange(1, width+1)

    # Unwrap image arrays to 1 dimensional arrays
    sig1 = np.ravel(im1)
    sig2 = np.ravel(im2)

    # Perform a continuous wavelet transform (cwt) on each array
    # Use Ricker (a.k.a. Mexican Hat a.k.a. Marr) wavelet
    # Ricker is neg. normalized 2nd derivative of a Gaussian
    cwtmatr1 = signal.cwt(sig1, signal.ricker, widths)
    cwtmatr2 = signal.cwt(sig2, signal.ricker, widths)

    # Compute the first term:
    # Compute product of the absolute values of the cwts
    c1c2 = np.multiply(abs(cwtmatr1), abs(cwtmatr2))
    # Compute squares of absolute values of the cwt for each image
    c1_2 = np.square(abs(cwtmatr1))
    c2_2 = np.square(abs(cwtmatr2))
    num_ssim_1 = 2 * np.sum(c1c2, axis=0) + 0.01
    den_ssim_1 = np.sum(c1_2, axis=0) + np.sum(c2_2, axis=0) + 0.01
    # Compute the second term:
    """
    Compute consistency of phase changes between the arrays.
    Structural info of local features is concentrated in the relative
    phase patterns of the wavelet coefficients (i.e. a consistent
    phase shift of all coefficients does not change the structure of
    the local image feature. First compute the product of the cwt of
    the first image and the complex conjugate of the cwt of the second image:
    """
    c1c2_conj = np.multiply(cwtmatr1, np.conjugate(cwtmatr2))
    num_ssim_2 = 2 * np.abs(np.sum(c1c2_conj, axis=0)) + 0.01
    den_ssim_2 = 2 * np.sum(np.abs(c1c2_conj), axis=0) + 0.01

    # Compute Index and Mean
    cw_ssim_map = (num_ssim_1 / den_ssim_1) * (num_ssim_2 / den_ssim_2)
    cw_ssim_map = cw_ssim_map.reshape(im1.shape[0],
                                      im1.shape[1])
    cw_ssim_index = round(np.average(cw_ssim_map), 3)

    end = timer()
    print("...Complete. Elapsed Time: " + str((end - start))[0:4])

    return cw_ssim_index, cw_ssim_map


def convolve(image, kernel):
    """ Perform Convolution on Image with a given kernel.

    Parameters
    ----------
    image : ndarray
        Image.  Any dimensionality.
    kernel : ndarray
        Kernel to convolve over image.

    Returns
    -------
    output : ndarray
        Convolved Image.
    """

    # grab the spatial dimensions of the image, along with
    # the spatial dimensions of the kernel
    (iH, iW) = image.shape[:2]
    (kH, kW) = kernel.shape[:2]

    # allocate memory for the output image, taking care to
    # "pad_size" the borders of the input image so the spatial
    # size (i.e., width and height) are not reduced

    pad_size = int((kW - 1) / 2)
    image = pad(image, pad_size, mode='edge')
    output = np.zeros((iH, iW), dtype="float32")

    # loop over the input image, "sliding" the kernel across
    # each (x, y)-coordinate from left-to-right and top to
    # bottom

    for y in np.arange(pad_size, iH + pad_size):
        for x in np.arange(pad_size, iW + pad_size):
            # extract the ROI of the image by extracting the
            # *center* region of the current (x, y)-coordinates
            # dimensions

            roi = image[y - pad_size:y + pad_size + 1, x - pad_size:x + pad_size + 1]

            # perform the actual convolution by taking the
            # element-wise product between the ROI and
            # the kernel, then summing the matrix

            k = (roi * kernel).sum()

            # store the convolved value in the output (x,y)
            # coordinate of the output image
            output[y - pad_size, x - pad_size] = k
    return output


def compute_gms(im1, im2):
    """ Compute the Gradient Magnitude Similarity (GMS) and
    Deviation Index (GMSD) of two images.

    A GMSD of 1 indicates perfect similarity. A GMSD of 0 is the
    lower bound for poor similarity.
    Xue, W., Zhang, L., Mou, X., & Bovik, A. C. (2014).
    Gradient magnitude similarity deviation: A highly efficient perceptual
    image quality index.
    IEEE Transactions on Image Processing, 23(2), 668–695.
    http://doi.org/10.1109/TIP.2013.2293423

    Args:
        im1 (ndarray): 2d array for similarity
        im2 (ndarray): 2d array, same size/shape as im1
    Returns:
        gms_index (float): The GMSD metric.
    gms_map (ndarray) GMS Array.
    """

    print("Computing Gradient Magnitude Similarity...")
    start = timer()
    # Construct Prewitt kernels with values from literature
    h_x = [0.33, 0, -0.33, 0.33, 0, -0.33, 0.33, 0, -0.33]
    h_x = np.array(h_x).reshape(3, 3)
    h_y = np.flipud(np.rot90(h_x))

    # Create gradient magnitude images for each image with Prewitt kernels
    # Reference (im1)
    ref_conv_hx = convolve(im1, h_x)
    ref_conv_hy = convolve(im1, h_y)
    ref_grad_mag = np.sqrt((ref_conv_hx ** 2) + (ref_conv_hy ** 2))

    # 'Distorted' (im2)
    dst_conv_hx = convolve(im2, h_x)
    dst_conv_hy = convolve(im2, h_y)
    dst_grad_mag = np.sqrt((dst_conv_hx ** 2) + (dst_conv_hy ** 2))

    c = 0.0026  # Constant provided by literature

    gms_map = (2 * ref_grad_mag * dst_grad_mag + c) / (ref_grad_mag ** 2 + dst_grad_mag ** 2 + c)
    gms_index = np.sqrt(np.sum((gms_map - gms_map.mean()) ** 2) / gms_map.size)

    end = timer()
    print("...Complete. Elapsed Time [s]: " + str(end - start))

    return round(gms_index, 3), gms_map


def compute_all_iqa(im1, im2):
    """ Compute all similarity metrics and maps and return a dictionary.

    """

    sim = dict()
    sim['nrmse'], sim['nrmse_arr'] = compute_mse(im1, im2)
    sim['ssim'], sim['ssim_arr'] = compute_ssim(im1, im2, 3)
    sim['cwssim'], sim['cwssim_arr'] = cw_ssim(im1, im2, 30)
    sim['gmsd'], sim['gms_arr'] = compute_gms(im1, im2)
    # sim['fsim_value'], sim['pc_max_map'] = compute_fsim(im1, im2)

    return sim
