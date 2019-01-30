#
import numpy as np
from scipy import signal
from timeit import default_timer as timer


def cw_ssim(reference, target, width):

        """Compute the complex wavelet SSIM (CW-SSIM) value from the reference
        image to the target image.
        Args:
          reference and target images
          width: width for the wavelet convolution (default: 30)
        Returns:
          Computed CW-SSIM float value and map.
        """

        # Define a width for the wavelet convolution
        widths = np.arange(1, width+1)

        # Use the image data as arrays
        sig1 = np.ravel(reference)
        sig2 = np.ravel(target)

        # Convolution
        cwtmatr1 = signal.cwt(sig1, signal.ricker, widths)
        cwtmatr2 = signal.cwt(sig2, signal.ricker, widths)

        # Compute the first term
        c1c2 = np.multiply(abs(cwtmatr1), abs(cwtmatr2))
        c1_2 = np.square(abs(cwtmatr1))
        c2_2 = np.square(abs(cwtmatr2))
        num_ssim_1 = 2 * np.sum(c1c2, axis=0) + 0.01
        den_ssim_1 = np.sum(c1_2, axis=0) + np.sum(c2_2, axis=0) + 0.01

        # Compute the second term
        c1c2_conj = np.multiply(cwtmatr1, np.conjugate(cwtmatr2))
        num_ssim_2 = 2 * np.abs(np.sum(c1c2_conj, axis=0)) + 0.01
        den_ssim_2 = 2 * np.sum(np.abs(c1c2_conj), axis=0) + 0.01

        # Construct the result
        cw_ssim_map = (num_ssim_1 / den_ssim_1) * (num_ssim_2 / den_ssim_2)
        cw_ssim_map = cw_ssim_map.reshape(reference.shape[0],
                                          reference.shape[1])

        # Average the per pixel results
        cw_ssim_index = round(np.average(cw_ssim_map), 3)

        return cw_ssim_index, cw_ssim_map

# def compute_cw_ssim(im1, im2, width):
#     """
#     Compute a complex wavelet implementation of SSIM (CW-SSIM).
#
#     CW-SSIM insensitive to translation, scaling and rotation of
#     images. A value of +1 indicates perfect similarity and a value of
#     -1 indicates lack of similarity.
#
#     Args:
#         im1 (ndarray): 2d array for similarity
#         im2 (ndarray): 2d array, same size/shape as im1
#         width (int): wavelet width for convolution (default: 30)
#     Returns:
#         ssim (tuple): mean value and array of CW-SSIM values
#     Raises:
#         Exception: description
#     """
#     start = timer()
#     print("Computing CW-SSIM...")
#
#     # Define a width for the wavelet convolution
#
#     widths = np.arange(1, width + 1)
#
#     # Unwrap image arrays to 1 dimensional arrays
#
#     sig1 = np.ravel(im1)
#     sig2 = np.ravel(im2)
#
#     # Perform a continuous wavelet transform (cwt) on each array
#     # Use Ricker (a.k.a. Mexican Hat a.k.a. Marr) wavelet
#     # Ricker is neg. normalized 2nd derivative of a Gaussian function
#
#     cwt1 = signal.cwt(sig1, signal.ricker, widths)
#     cwt2 = signal.cwt(sig2, signal.ricker, widths)
#
#     # Compute product of the absolute values of the cwts
#
#     abscwt1_abscwt2 = np.multiply(abs(cwt1), abs(cwt2))
#
#     # Compute the square of of the absolute values of the cwt for each image
#
#     cwt1_abs_square = np.square(abs(cwt1))
#     cwt2_abs_square = np.square(abs(cwt2))
#     # First component of equation (REF)
#     comp1_top = 2 * np.sum(abscwt1_abscwt2, axis=0) + 0.01
#     comp1_bottom = np.sum(cwt1_abs_square, axis=0)
#     + np.sum(cwt2_abs_square, axis=0) + 0.01
#     comp1 = comp1_top / comp1_bottom
#
#     """
#     Compute consistency of phase changes between the arrays.
#     Structural info of local features is concentrated in the relative
#     phase patterns of the wavelet coefficients (i.e. a consistent
#     phase shift of all coefficients does not change the structure of
#     the local image feature. First compute the product of the cwt of
#     the first image and the complex conjugate of the cwt of the second image:
#     """
#     cwt1_conj_cwt2 = np.multiply(cwt1, np.conjugate(cwt2))
#
#     # Second Component of EQN (ref)
#     comp2_top = 2 * np.abs(np.sum(cwt1_conj_cwt2, axis=0)) + 0.01
#     comp2_bottom = 2 * np.sum(np.abs(cwt1_conj_cwt2), axis=0) + 0.01
#     comp2 = comp2_top / comp2_bottom
#
#     # Compute the CW-SSIM index
#
#     cw_ssim_map = (comp1 * comp2).reshape(im1.shape[0], im1.shape[1])
#
#     # Average the per pixel results
#
#     cw_ssim_index = round(cw_ssim_map.mean(), 3)
#
#     return cw_ssim_index, cw_ssim_map
#
#     end = timer()
#     print("...Complete. Elapsed Time [s]: " + str(end - start))
