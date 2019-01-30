#
from .all_metrics_in_one import compute_mse
from .all_metrics_in_one import compute_ssim
from .all_metrics_in_one import cw_ssim
from .all_metrics_in_one import compute_gms
# from similarity_tests.feature_similarity import compute_fsim


def compute_similarity(im1, im2):
    """ Compute all similarity metrics and maps and return a dictionary.

    """

    sim = dict()
    sim['nrmse'], sim['nrmse_arr'] = compute_mse(im1, im2)
    sim['ssim'], sim['ssim_arr'] = compute_ssim(im1, im2, 3)
    sim['cwssim'], sim['cwssim_arr'] = cw_ssim(im1, im2, 30)
    sim['gmsd'], sim['gms_arr'] = compute_gms(im1, im2)
    # sim['fsim_value'], sim['pc_max_map'] = compute_fsim(im1, im2)

    return sim
