"""Return qualis for papers from a assigned csv."""

import pandas as pd
# from resources.support_functions import qualis_file


def paperqualis(ls_per_issn, qf):
    """Return qualis for papers from a assigned csv."""
    # qf = qualis_file()
    ls_paperqualis = []
    path_qualis = './jcr_qualis/' + qf
    df_qualis = pd.read_csv(path_qualis,
                            header=0, sep='\t')
    for idq in range(len(ls_per_issn)):
        issn = ls_per_issn[idq]
        issn = str(issn[0:4]) + '-' + str(issn[4:])
        result = df_qualis[df_qualis['ISSN'] == issn].reset_index(drop=True)
        if len(result) == 0:
            qualis = 'XX'
        else:
            qualis = result.iloc[0, 2]
        ls_paperqualis.append(qualis)
        # print(qualis)
    return ls_paperqualis
