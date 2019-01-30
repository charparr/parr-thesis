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
    print("...Complete. Elapsed Time: [s] " + str((end - start)))

    return round(mse_value, 3), square_error_map
