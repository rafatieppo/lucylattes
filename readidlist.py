import pandas as pd


def readIdList():
    df_idnamelist = pd.read_csv('list_id_name.csv',
                                skiprows=3, header=0)
    return(df_idnamelist)    
