# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import glob
import re
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Producao bibliografica
# ------------------------------------------------------------

lscsv_paper = glob.glob('./csv_producao/*period.csv')
len(lscsv_paper)
dfpaper = pd.DataFrame()
lsid = []
for i in range(len(lscsv_paper)):
    a = pd.read_csv(lscsv_paper[i], header=0)
    dfpaper = dfpaper.append(a, ignore_index=False)
    id = lscsv_paper[i].split('_')[1].split('/')[1]
    idrep = np.repeat(id, len(a['TITLE']))
    print(id, len(a['TITLE']))
    lsid.append(idrep)
dfpaper['ID'] = np.concatenate(lsid)
lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
len(lscsv_fullname)
# df com nome completo, sobrenome e id
dffullname = pd.DataFrame()
for i in range(len(lscsv_fullname)):
    a = pd.read_csv(lscsv_fullname[i], header=0)
    dffullname = dffullname.append(a, ignore_index=False)
# processo para excluir paper repetido busca o sobrenome do autor no
# dffullname por meio do id lattes. divide a coluna autores do
# paper. verifica a ordem do sobrenome no author_split
lsauthor_order = []
order = -99
for i in range(len(dfpaper['ID'])):
    lastname = dffullname[dffullname['ID']
                          == float(dfpaper.iloc[i, 9])]
    lastname = lastname.iloc[0, 2]
    author_split = dfpaper.iloc[i, 7].split(',')
    # print(lastname)
    # print(len(author_split))
    for aa in range(len(author_split)):
        test = lastname in author_split[aa]
        if test == True:
            order = aa + 1
    lsauthor_order.append(order)
dfpaper['OR'] = lsauthor_order
# retirando paper repetido, fica para o author com maior importancia
dfpaper_uniq = dfpaper.sort_values(['OR'])
dfpaper_uniq.drop_duplicates(['TITLE'], inplace=True)
# ------------------------------------------------------------
# filtrando o ano
config_file = open('./config.txt', 'r')
yyi = config_file.readlines()[5].split(':')[1]
yyi = yyi.rstrip('\n')
yyi = yyi.strip(' ')
yyi = float(yyi)
config_file.close()
dfpaper = dfpaper[dfpaper['YEAR'] >= yyi]
dfpaper_uniq = dfpaper_uniq[dfpaper_uniq['YEAR'] >= yyi]
# ------------------------------------------------------------
# artig completo periodico
acp = dfpaper_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
acp = acp['TITLE'].sum()
