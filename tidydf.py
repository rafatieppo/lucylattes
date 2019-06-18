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
        iid = str(lscsv_ppe[i].split('_')[1].split('/')[1])
        idrep = np.repeat(iid, len(a['PROJ']))
        # print(iid, len(a['PROJ']))
        lsid.append(idrep)
    dfppe['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    # df com nome completo, sobrenome e iid
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
        # passando ID para string, para poder comparar com dfpaper
        # cancelei a ss() pq o read_csv do a esta com dtype='str
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dfppe = pd.merge(dfppe, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PROJETOS repetido busca o sobrenome do autor no
    # dffullname por meio do iid lattes. divide a coluna autores do
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
        iid = str(lscsv_paper[i].split('_')[1].split('/')[1])
        idrep = np.repeat(iid, len(a['TITLE']))
        # print(iid, len(a['TITLE']))
        lsid.append(idrep)
    dfpaper['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    # df com nome completo, sobrenome e iid
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    # passando IID para string, para poder comparar com dfpaper
    # cancelei a ss() pq o read_csv do a esta com dtype='str
    # dffullname['ID'] = dffullname['ID'].apply(ss)
    dfpaper = pd.merge(dfpaper, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PAPER repetido busca o sobrenome do autor no
    # dffullname por meio do iid lattes. divide a coluna autores do
    # paper.
    # atual: a ordem já vem no dfpaper
    # antiga: verifica a ordem do sobrenome no author_split
    #lsauthor_order = []
    #order = -99
    # for i in range(len(dfpaper['ID'])):
    #     lastname = dffullname[dffullname['ID']
    #                           == (dfpaper.iloc[i, 9])]
    #     lastname = lastname.iloc[0, 2]
    #     author_split = dfpaper.iloc[i, 7].split(',')
    #     # print(lastname)
    #     # print(len(author_split))
    #     for aa in range(len(author_split)):
    #         test = lastname in author_split[aa]
    #         if test == True:
    #             order = aa + 1
    #     lsauthor_order.append(order)
    #dfpaper['OR'] = lsauthor_order
    # retirando paper repetido, fica para o author com maior importancia
    dfpaper_uniq = dfpaper.sort_values(['ORDER_OK'])
    dfpaper_uniq.drop_duplicates(['TITLE'], inplace=True)
    pathfilename = str('./csv_producao/periodicos_all.csv')
    dfpaper.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper['TITLE']), ' artigos')
    pathfilename = str('./csv_producao/periodicos_uniq.csv')
    dfpaper_uniq.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper_uniq['TITLE']), ' artigos')

    # ------------------------------------------------------------
    # Producao bibliografica LIVROS
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_book = glob.glob('./csv_producao/*livro.csv')
    if len(lscsv_book) < 1:
        print('Producao de livros nao encontrada')
    else:
        dfbook = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_book)):
            a = pd.read_csv(lscsv_book[i], header=0)
            dfbook = dfbook.append(a, ignore_index=False)
            iid = str(lscsv_book[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['TITLE']))
            # print(iid, len(a['TITLE']))
            lsid.append(idrep)
        dfbook['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
            # passando IID para string, para poder comparar com dfbook
            # cancelei a ss() pq o read_csv do a esta com dtype='str
            # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfbook = pd.merge(dfbook, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        dfbook_uniq = dfbook.sort_values(['ORDER_OK'])
        dfbook_uniq.drop_duplicates(['TITLE'], inplace=True)
        pathfilename = str('./csv_producao/livros_all.csv')
        dfbook.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfbook['TITLE']), ' livros')
        pathfilename = str('./csv_producao/livros_uniq.csv')
        dfbook_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfbook_uniq['TITLE']), ' livros')

    # ------------------------------------------------------------
    # Producao bibliografica CAPITULOS
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_chapter = glob.glob('./csv_producao/*capitulo.csv')
    if len(lscsv_chapter) < 1:
        print('Producao de capitulos nao encontrada')
    else:
        dfchapter = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_chapter)):
            a = pd.read_csv(lscsv_chapter[i], header=0)
            dfchapter = dfchapter.append(a, ignore_index=False)
            iid = str(lscsv_chapter[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['TITLE']))
            # print(iid, len(a['TITLE']))
            lsid.append(idrep)
        dfchapter['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
        # passando IID para string, para poder comparar com dfchapter
        # cancelei a ss() pq o read_csv do a esta com dtype='str
        # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfchapter = pd.merge(dfchapter, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        dfchapter_uniq = dfchapter.sort_values(['ORDER_OK'])
        dfchapter_uniq.drop_duplicates(['TITLE'], inplace=True)
        pathfilename = str('./csv_producao/capitulos_all.csv')
        dfchapter.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfchapter['TITLE']), ' capitulos de livros')
        pathfilename = str('./csv_producao/capitulos_uniq.csv')
        dfchapter_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfchapter_uniq['TITLE']), ' capitulos de livros')

    # ------------------------------------------------------------
    # ORIENTACAO TCC IC MESTRADO DOUTORADO
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_advi = glob.glob('./csv_producao/*advis.csv')
    if len(lscsv_advi) < 1:
        print('Orientacao para TCC, IC, MESTRADO ou DOUTORADO nao encontrada')
    else:
        dfadvi = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_advi)):
            a = pd.read_csv(lscsv_advi[i], header=0)
            dfadvi = dfadvi.append(a, ignore_index=False)
            iid = str(lscsv_advi[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['YEAR']))
            # print(iid, len(a['TITLE']))
            lsid.append(idrep)
        dfadvi['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        # len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
            # passando IID para string, para poder comparar com dfadvi
            # cancelei a ss() pq o read_csv do a esta com dtype='str
            # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfadvi = pd.merge(dfadvi, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        pathfilename = str('./csv_producao/orientacoes_all.csv')
        dfadvi.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfadvi['YEAR']), ' orientacoes')
