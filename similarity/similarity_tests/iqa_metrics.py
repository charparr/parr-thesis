import numpy as np
from scipy import signal
from skimage.util import pad
from skimage.measure import compare_ssim
from timeit import default_timer as timer


def compute_nrmse(im1, im2):
    """
    Compute the Normalized Mean Square Error.

    A min-max normalized mean square error value and array are computed from
    two input images (i.e. patterns). This implementation ignores the order of
    im1 and im2 in the normalization. We normalize to scale values between 0
    and 1, and then subtract both the global value and the array from 1 so
    that higher values indicate a greater degree of similarity (i.e. less
    error) between the two images.

    Args:
        im1 (ndarray): 2d array
        im2 (ndarray): 2d array, same size/shape/type as im1
    Returns:
        nrmse (tuple): nrmse value and array of nrsme values
    Raises:
        Exception: description
    """
    print("Computing NRMSE...")
    start = timer()

    im1_max = np.nanmax(im1)
    im2_max = np.nanmax(im2)
    im1_min = np.nanmin(im1)
    im2_min = np.nanmin(im2)
    both_max = max(im1_max, im2_max)
    both_min = min(im1_min, im2_min)

    # Compute global index NRMSE value
    mse = np.mean(np.square(im1 - im2))
    min_max_nrmse = np.sqrt(mse) / (both_max - both_min)
    # Compute NRSE array
    square_error = np.square(im1 - im2)
    min_max_nrmse_arr = np.sqrt(square_error) / (both_max - both_min)
    # Reverse scale so 1 is 'good', 0 is 'bad'
    nrmse_flip = round(1 - min_max_nrmse, 3)
    nrmse_arr_flip = 1 - min_max_nrmse_arr

    nrmse_results = (nrmse_flip, nrmse_arr_flip)

    print("Complete. " + str((timer() - start))[0:4] + " s")

    return nrmse_results


def compute_ssim(im1, im2):
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
    Returns:
        ssim (tuple): mean value and array of SSIM values
    Raises:
        Exception: description
    """

    start = timer()
    print("Computing SSIM...")
    mean_ssim_val, ssim_arr = compare_ssim(im1, im2,
                                           sigma=1.5,
                                           gaussian_weights=True,
                                           use_sample_covariance=False,
                                           full=True)

    mean_ssim_val_scaled = (mean_ssim_val + 1) / 2
    ssim_arr_scaled = (ssim_arr + 1) / 2
    ssim = (mean_ssim_val_scaled, ssim_arr_scaled)

    print("Complete. " + str((timer() - start))[0:4] + " s")

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
    print("Computing Complex Wavelet SSIM...")

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

    print("Complete. " + str((timer() - start))[0:4] + " s")

    return (cw_ssim_index + 1) / 2, (cw_ssim_map + 1) / 2


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

            roi = image[y - pad_size:y + pad_size + 1, x - pad_size:x
                        + pad_size + 1]

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
    print("...Complete. Elapsed Seconds: " + str((end - start))[0:4])

    return 1 - round(gms_index, 3), gms_map


def compute_all_iqa(im1, im2):
    """
    Compute all similarity metrics and maps and return a dictionary.

    Calls all simliarity metrics (IQA) on an image pair. Current metrics: MSE,
    SSIM, CW-SSIM, and GMS).
    Args:
        im1 (ndarray): 2d array for similarity
        im2 (ndarray): 2d array, same size/shape as im1
    Returns:
        sim (dict): dictionary that stores results with the following
        structure: results{
                    [*metric*: float,
                    *metric*_arr: array]}
    Raises:
        None.
    """
    sim = dict()
    sim['nrmse'], sim['nrmse_arr'] = compute_nrmse(im1, im2)
    sim['ssim'], sim['ssim_arr'] = compute_ssim(im1, im2)
    sim['cwssim'], sim['cwssim_arr'] = cw_ssim(im1, im2, 10)
    sim['gms'], sim['gms_arr'] = compute_gms(im1, im2)
    # sim['fsim_value'], sim['pc_max_map'] = compute_fsim(im1, im2)
    return sim
