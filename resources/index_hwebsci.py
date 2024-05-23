"""Script to run function index_h for researcher and group."""

import glob
import re
from resources.support_functions_indexh import index_h
from resources.support_functions_indexh import index_h_allgroup
from resources.support_functions import yearlimit_forfilter
import numpy as np
import pandas as pd


def getindex_hwebsci():
    """Tidy data for index h calculations."""
    # list of ids
    zipfiles = glob.glob('./csv_webofsci/*_webofsci.csv')
    lsids = []
    for idx in range(len(zipfiles)):
        nl = re.findall('[0-9]', zipfiles[idx])
        nl = ''.join(nl)
        lsids.append(nl)
    # lendo ano minimo maximo para selecao
    lsyear_limits = yearlimit_forfilter()
    yyi, yyf = lsyear_limits[0], lsyear_limits[1]
    # lendo os arquivos hwebsci
    dfhwebsci = pd.DataFrame()
    for nid in range(len(lsids)):
        hwebofscifilename = str(
            './csv_webofsci/' + lsids[nid]) + '_webofsci.csv'
        df_temp = pd.read_csv(hwebofscifilename, sep=',', header=0,
                              skiprows=10)
        df_temp['ID_LATTES'] = np.repeat(lsids[nid], len(df_temp))
        dfhwebsci = pd.concat([dfhwebsci, df_temp], axis=0)

    # filtro da base de artigo em funcao do ano desejado
    # dfhwebsci = dfhwebsci[(dfhwebsci['Publication Year'] >= yyi) &
    #                       (dfhwebsci['Publication Year'] <= yyf)]
    dfhwebsci = dfhwebsci.reset_index(drop=True)

    # merge a fullname columns
    dffullname = pd.read_csv('./csv_producao/fullname_all.csv',
                             header=0, dtype='str')

    # creating a col for nickname in plots
    dffullname['NICKNAME'] = [str(xx.split(' ')[-1] +
                                  xx.split(' ')[0][0:4])
                              for xx in dffullname['FULL_NAME'].to_list()]
    # merger with fullname
    dfhwebsci = pd.merge(dfhwebsci, dffullname,
                         left_on='ID_LATTES', right_on='ID')

    dfhwebsci.to_csv(
        './csv_producao_hindex/hindex_websci_papers.csv', index=False)

    # ------------------------------------------------------------
    # df for dropped papers
    dfhwebsci_uniq = dfhwebsci.copy()
    # dropping duplicates titles
    ls_position = []
    for i in range(len(dfhwebsci_uniq)):
        lastname = dfhwebsci_uniq['FULL_NAME'].iloc[i].split(' ')[-1]
        lastname
        mm = dfhwebsci_uniq['Authors'].iloc[i]
        mm = mm.replace(",", "")
        mm = mm.split(";")
        # [s for s in mm if lastname in s]
        for j in range(len(mm)):
            if lastname in mm[j]:
                position = j + 1
                break
            else:
                position = -99
        ls_position.append(position)
    dfhwebsci_uniq['POSITION'] = ls_position
    dfhwebsci_uniq.sort_values(['Title', 'POSITION'], inplace=True)
    dfhwebsci_uniq = dfhwebsci_uniq.reset_index(drop=True)
    dfhwebsci_uniq.drop_duplicates(subset=['Title'], inplace=True)
    dfhwebsci_uniq = dfhwebsci_uniq.reset_index(drop=True)
    dfhwebsci_uniq.to_csv(
        './csv_producao_hindex/hindex_websci_papers_uniq.csv',
        index=False, sep=',')

    # func for h index with all papers for all researchers
    index_h(lsids, dfhwebsci, dffullname, 'hindex_websci_papers_tbl')

    # func for h index with no duplicate papers
    index_h(lsids, dfhwebsci_uniq, dffullname, 'hindex_websci_papers_tbl_uniq')

    # funcao para indice H p/ dados c/ remocao de artigos duplicados para GRUPO
    index_h_allgroup(dfhwebsci_uniq)

    print("\n\n Index H WebofSci gerado com sucesso")
