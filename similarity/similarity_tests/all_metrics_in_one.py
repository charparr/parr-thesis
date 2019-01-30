from skimage.measure import compare_nrmse
from timeit import default_timer as timer

## PUT ALL metric functions here:


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

    return round(mse_value, 3), square_error_map

    end = timer()
    print("...Complete. Elapsed Time: [s] " + str((end - start)))


def compute_ssim(im1, im2, win_size):
    """
    Calculate the Structural Similarity of two single band images.
    The two input images must be the same size and shape.
    Parameters:
        im1: Single band image (array)
        im2: Single band image(array)
        win_size: length of the sliding comparison window. must be odd. (int)
    A valid comparison will return two objects:
    1.) A Mean Global Structural Similarity Value
    2.) The map (array) of element-wise structural similarity.
    The Structural Similarity Index Method (SSIM) is a technique grounded in the idea that the human visual system is
    well adapted to extracting structural information from a scene. From Wang et al., 2004:
    "We define structural information in an image as those attributes that represent the structure of objects in the
    scene, independent of the average luminance and contrast. Since luminance and contrast can vary across a scene, we
    use the local luminance and contrast for our definition. Luminance, contrast, and structure comparisons make up the
    SSIM method.
    Brightness in the SSIM map indicates the magnitude of the local SSIM index (squared for visibility).

     Wang, Z., Bovik, A. C., Sheikh, H. R., & Simoncelli, E. P. (2004). Image quality assessment: From error visibility to structural similarity. IEEE Transactions on Image Processing, 13, 600-612. https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf, DOI:10.1109/TIP.2003.819861
    """

    start = timer()
    if win_size % 2 != 1:
        print('Please provide an odd integer for the window size.')
    else:
        print("Computing Structural Similarity Index...")
        ssim = compare_ssim(im1, im2, win_size=win_size, full=True)

        end = timer()
        print("...Complete. Elapsed Time: " + str((end - start)))

        return ssim
