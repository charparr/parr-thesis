#from similarity_tests.gradient_magnitude import compute_gms
#from similarity_tests.feature_similarity import compute_fsim
from .mean_square_error import compute_mse
from .structural_similarity import compute_ssim
from .complex_wavelet_ssim import compute_cw_ssim, cw_ssim


def compute_similarity(im1, im2):
    """ Compute all similarity metrics and maps.

    """

    sim = dict()
    sim['nrmse_val'], sim['nrmse_arr'] = compute_mse(im1, im2)
    sim['ssim_val'], sim['ssim_arr'] = compute_ssim(im1, im2, 3)
    sim['cwssim_val'], sim['cwssim_arr'] = cw_ssim(im1, im2, 30)
    # results['gms_value'], results['gms_map'] = compute_gms(im1, im2)
    # # results['fsim_value'], results['pc_max_map'] = compute_fsim(im1, im2)
    #
    return sim
