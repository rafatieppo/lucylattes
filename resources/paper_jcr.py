"""Return jcr for papers from a assigned csv."""

import pandas as pd


def paperjcr(ls_per_issn):
    """Return jcr for papers from a assigned csv."""
    path_jcr = './jcr_qualis/jcr_factor.csv'
    df_jcr = pd.read_csv(path_jcr, sep=',', header=0, dtype='str')
    ls_jcr = []
    for idq in range(len(ls_per_issn)):
        issn = ls_per_issn[idq]
        result = df_jcr[df_jcr['ISSN_A'] == issn].reset_index(drop=True)
        if len(result) == 0:
            result = df_jcr[df_jcr['ISSN_B'] == issn].reset_index(drop=True)
            if len(result) == 0:
                jcr = -99
            else:
                jcr = result.iloc[0, 7]
        else:
            jcr = result.iloc[0, 7]
        ls_jcr.append(jcr)
    return ls_jcr
