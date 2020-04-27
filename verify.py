# ------------------------------------------------------------
# packages
# ------------------------------------------------------------
# ------------------------------------------------------------
from extrafuns import *
from tabulate import tabulate
import numpy as np
import pandas as pd
import os
import glob
import re
import matplotlib.pyplot as plt
import matplotlib.style as style
import sys
style.available
style.use('fivethirtyeight')


def getverificacao():
    # ------------------------------------------------------------
    # vericando se ha arquivos csv gerados pelo gettidy e excluindo NaN
    # ------------------------------------------------------------
    # dfppe_all
    try:
        dfppe_all = pd.read_csv('./csv_producao/projetos_all.csv',
                                header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao de proj. pesq ou ext. \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfppe_all['PROJ'])):
            si = dfppe_all.iloc[i, 1]
            if pd.isna(si) or si == 'VAZIO':
                print('------------------------------------------------------------\n' +
                      'ATENCAO \n' +
                      'Impossível extrair ANO para o projeto \n' +
                      str(dfppe_all.iloc[i, 0]) + ' \n do pesquisador: ' +
                      str(dfppe_all.iloc[i, 7]) + '... PROJETO EXCLUIDO \n' +
                      str('ano inicial do projeto nao declarado \n') +
                      '------------------------------------------------------------')
                lsind.append(i)
            else:
                si = int(float(si))
        dfppe_all.drop(lsind, axis=0, inplace=True)
        dfppe_all.reset_index()
        pathfilename = str('./csv_producao/projetos_all.csv')
        dfppe_all.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfppe_uniq
    try:
        dfppe_uniq = pd.read_csv('./csv_producao/projetos_uniq.csv',
                                 header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao de proj. pesq ou ext. uniq \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfppe_uniq['YEAR_INI'])):
            si = dfppe_uniq.iloc[i, 1]
            try:
                int(si)
                si = int(si)
            except ValueError:
                lsind.append(i)
        dfppe_uniq.drop(lsind, axis=0, inplace=True)
        dfppe_uniq.reset_index()
        pathfilename = str('./csv_producao/projetos_uniq.csv')
        dfppe_uniq.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfpaper
    try:
        dfpaper = pd.read_csv('./csv_producao/periodicos_all.csv',
                              header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com periodicos all \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfpaper['YEAR'])):
            si = dfpaper.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                print('------------------------------------------------------------\n' +
                      'ATENCAO \n' +
                      'Impossível extrair ANO para o paper \n' +
                      str(dfpaper.iloc[i, 0]) + ' \n do autor: ' +
                      str(dfpaper.iloc[i, 11]) + '... PAPER EXCLUIDO \n'
                      '------------------------------------------------------------')
                # sys.exit("Verique o lattes do autor")
                lsind.append(i)
        dfpaper.drop(lsind, axis=0, inplace=True)
        dfpaper.reset_index()
        pathfilename = str('./csv_producao/periodicos_all.csv')
        dfpaper.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfpaper_uniq
    try:
        dfpaper_uniq = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                                   header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com periodicos unique \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfpaper_uniq['YEAR'])):
            si = dfpaper_uniq.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                lsind.append(i)
        dfpaper_uniq.drop(lsind, axis=0, inplace=True)
        dfpaper_uniq.reset_index()
        pathfilename = str('./csv_producao/periodicos_uniq.csv')
        dfpaper_uniq.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfbooks
    try:
        dfbooks = pd.read_csv('./csv_producao/livros_all.csv',
                              header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao livros all \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfbooks['YEAR'])):
            si = dfbooks.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                print('------------------------------------------------------------\n' +
                      'ATENCAO \n' +
                      'Impossível extrair ANO para o livro \n' +
                      str(dfbooks.iloc[i, 0]) + ' \n do autor: ' +
                      str(dfbooks.iloc[i, 11]) + '... LIVRO EXCLUIDO \n'
                      '------------------------------------------------------------')
                # sys.exit("Verique o lattes do autor")
                lsind.append(i)
        dfbooks.drop(lsind, axis=0, inplace=True)
        dfbooks.reset_index()
        pathfilename = str('./csv_producao/livros_all.csv')
        dfbooks.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfbooks uniq
    try:
        dfbooks_uniq = pd.read_csv('./csv_producao/livros_uniq.csv',
                                   header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao de livros unique \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfbooks_uniq['YEAR'])):
            si = dfbooks_uniq.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                lsind.append(i)
        dfbooks_uniq.drop(lsind, axis=0, inplace=True)
        dfbooks_uniq.reset_index()
        pathfilename = str('./csv_producao/livros_uniq.csv')
        dfbooks_uniq.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfchapter
    try:
        dfchapters = pd.read_csv('./csv_producao/capitulos_all.csv',
                                 header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao de capitulos all \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfchapters['YEAR'])):
            si = dfchapters.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                print('------------------------------------------------------------\n' +
                      'ATENCAO \n' +
                      'Impossível extrair ANO para o capitulo \n' +
                      str(dfchapters.iloc[i, 0]) + ' \n do autor: ' +
                      str(dfchapters.iloc[i, 11]) + '... CAPITULO EXCLUIDO \n'
                      '------------------------------------------------------------')
                # sys.exit("Verique o lattes do autor")
                lsind.append(i)
        dfchapters.drop(lsind, axis=0, inplace=True)
        dfchapters.reset_index()
        pathfilename = str('./csv_producao/capitulos_all.csv')
        dfchapters.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfchapters_uniq
    try:
        dfchapters_uniq = pd.read_csv('./csv_producao/capitulos_uniq.csv',
                                      header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com producao de capitulos unique \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfchapters_uniq['YEAR'])):
            si = dfchapters_uniq.iloc[i, 1]
            try:
                int(si)
            except ValueError:
                lsind.append(i)
        dfchapters_uniq.drop(lsind, axis=0, inplace=True)
        dfchapters_uniq.reset_index()
        pathfilename = str('./csv_producao/capitulos_uniq.csv')
        dfchapters_uniq.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfadvise FOR YEAR
    try:
        dfadvise = pd.read_csv('./csv_producao/orientacoes_all.csv',
                               header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com orientacoes \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfadvise['YEAR'])):
            si = dfadvise.iloc[i, 0]
            try:
                int(si)
            except ValueError:
                lsind.append(i)
        dfadvise.drop(lsind, axis=0, inplace=True)
        dfadvise.reset_index()
        pathfilename = str('./csv_producao/orientacoes_all.csv')
        dfadvise.to_csv(pathfilename, index=False)
    # ------------------------------------------------------------
    # dfadvise COURSE NAME
    try:
        dfadvise = pd.read_csv('./csv_producao/orientacoes_all.csv',
                               header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'Nao ha arquivo com orientacoes \n' +
              '------------------------------------------------------------')
    else:
        lsind = []
        for i in range(len(dfadvise['COURSE'])):
            si = dfadvise.iloc[i, 3]
            if pd.isna(si) or si == 'VAZIO':
                print('------------------------------------------------------------\n' +
                      'ATENCAO \n' +
                      'Impossível NOME CURSO para orientacao de \n' +
                      str(dfadvise.iloc[i, 4]) + ' \n do pesquisador: ' +
                      str(dfadvise.iloc[i, 8]) + '... PROJETO EXCLUIDO \n' +
                      str('ano inicial do projeto nao declarado \n') +
                      '------------------------------------------------------------')
                lsind.append(i)
            else:
                si = str(si)
        dfadvise.drop(lsind, axis=0, inplace=True)
        dfadvise.reset_index()
        pathfilename = str('./csv_producao/orientacoes_all.csv')
        dfadvise.to_csv(pathfilename, index=False)
