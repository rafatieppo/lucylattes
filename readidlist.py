import pandas as pd


def readIdList():
    df_idnamelist = pd.read_csv('list_id_name.txt', dtype='str',
                                skiprows=4, header=0,
                                sep=',')
    return(df_idnamelist)
# ------------------------------------------------------------
