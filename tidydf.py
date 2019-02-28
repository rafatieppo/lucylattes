# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import glob
import re
# ------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------

from extrafuns import *


def gettidydf():
    config_file = open('./config.txt', 'r')
    yyi = config_file.readlines()[5].split(':')[1]
    yyi = yyi.rstrip('\n')
    yyi = yyi.strip(' ')
    yyi = float(yyi)
    config_file.close()
    config_file = open('./config.txt', 'r')
    yyf = config_file.readlines()[6].split(':')[1]
    yyf = yyf.rstrip('\n')
    yyf = yyf.strip(' ')
    yyf = float(yyf)
    config_file.close()
    # ------------------------------------------------------------
    # Projetos de pesquisa e extensão
    # ------------------------------------------------------------
    # df com todos os projetos pesq e ext
    lscsv_ppe = glob.glob('./csv_producao/*_ppe.csv')
    dfppe = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_ppe)):
        a = pd.read_csv(lscsv_ppe[i], header=0)
        dfppe = dfppe.append(a, ignore_index=False)
        id = lscsv_ppe[i].split('_')[1].split('/')[1]
        idrep = np.repeat(id, len(a['PROJ']))
        print(id, len(a['PROJ']))
        lsid.append(idrep)
    dfppe['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    # df com nome completo, sobrenome e id
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0)
        dffullname = dffullname.append(a, ignore_index=False)
        # passando ID para string, para poder comparar com dfpaper
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dfppe = pd.merge(dfppe, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PROJETOS repetido busca o sobrenome do autor no
    # dffullname por meio do id lattes. divide a coluna autores do
    # paper. verifica a ordem do sobrenome no author_split
    lsauthor_order = []
    order = -99
    for i in range(len(dfppe['ID'])):
        lastname = dffullname[dffullname['ID']
                              == (dfppe.iloc[i, 6])]
        lastname = lastname.iloc[0, 2]
        author_split = dfppe.iloc[i, 7].split(',')
        # print(lastname)
        # print(len(author_split))
        for aa in range(len(author_split)):
            test = lastname in author_split[aa]
            if test == True:
                order = aa + 1
        lsauthor_order.append(order)
    dfppe['OR'] = lsauthor_order
    # retirando projeto repetido, fica para o author com maior importancia
    dfppe_uniq = dfppe.sort_values(['OR'])
    dfppe_uniq.drop_duplicates(['PROJ'], inplace=True)
    pathfilename = str('./csv_producao/projetos_all.csv')
    dfppe.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfppe['PROJ']), ' projetos')
    pathfilename = str('./csv_producao/projetos_uniq.csv')
    dfppe_uniq.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfppe_uniq['PROJ']), ' projetos')

    # ------------------------------------------------------------
    # Producao bibliografica
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_paper = glob.glob('./csv_producao/*period.csv')
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
    # passando ID para string, para poder comparar com dfpaper
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dfpaper = pd.merge(dfpaper, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PAPER repetido busca o sobrenome do autor no
    # dffullname por meio do id lattes. divide a coluna autores do
    # paper. verifica a ordem do sobrenome no author_split
    lsauthor_order = []
    order = -99
    for i in range(len(dfpaper['ID'])):
        lastname = dffullname[dffullname['ID']
                              == (dfpaper.iloc[i, 9])]
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
    pathfilename = str('./csv_producao/periodicos_all.csv')
    dfpaper.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper['TITLE']), ' artigos')
    pathfilename = str('./csv_producao/periodicos_uniq.csv')
    dfpaper_uniq.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper_uniq['TITLE']), ' artigos')
