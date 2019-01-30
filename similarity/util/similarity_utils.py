#
from itertools import combinations
import re


def create_pairs(d):
    '''
    This finds all unique combinations of years. The indexing chooses which
    image extent to use, i.e. source or roi for the comparisons.
    The pairs are stored in a comparison dictionary. Each key is a pair of
    observations from different years over the same location.
    '''

    rstr_pairs = {}
    # Create unique comparison pairs with others
    for key_pair in combinations(d.keys(), 2):
        yr_pair = ''.join(re.findall('(\d{4})', ''.join(key_pair)))
        y1 = yr_pair[:4]
        y2 = yr_pair[4:]
        yr_pair = y1 + ' v. ' + y2
        rstr_pairs[yr_pair] = {}
        rstr_pairs[yr_pair][y1] = {}
        rstr_pairs[yr_pair][y2] = {}
        rstr_pairs[yr_pair][y1]['arr'] = d[key_pair[0]]['arr']
        rstr_pairs[yr_pair][y2]['arr'] = d[key_pair[1]]['arr']

    # Create comparison pair with self
    for k in d.keys():
        yr = ''.join(d[k]['year'])
        smyr = yr + ' v. ' + yr
        rstr_pairs[smyr] = {}

        rstr_pairs[smyr][yr] = {}
        rstr_pairs[smyr][yr+'_'] = {}
        rstr_pairs[smyr][yr]['arr'] = d[k]['arr']
        rstr_pairs[smyr][yr+'_']['arr'] = d[k]['arr']
    return rstr_pairs
