# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

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
from tabulate import tabulate

from extrafuns import *


def getrelatorio():
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
    config_file = open('./config.txt', 'r')
    qualqualis = config_file.readlines()[4].split(':')[1]
    qualqualis = qualqualis.rstrip('\n')
    qualqualis = qualqualis.strip(' ')
    qualqualis = str(qualqualis)
    config_file.close()
    # ------------------------------------------------------------
    # importando os data frames gerados pelo gettidy
    # ------------------------------------------------------------
    dfppe_all = pd.read_csv('./csv_producao/projetos_all.csv',
                            header=0, dtype='str')
    dfppe_uniq = pd.read_csv('./csv_producao/projetos_uniq.csv',
                             header=0, dtype='str')
    dfpaper = pd.read_csv('./csv_producao/periodicos_all.csv',
                          header=0, dtype='str')
    dfpaper_uniq = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                               header=0, dtype='str')
    dfbooks = pd.read_csv('./csv_producao/livros_all.csv',
                          header=0, dtype='str')
    dfbooks_uniq = pd.read_csv('./csv_producao/livros_uniq.csv',
                               header=0, dtype='str')
    dfchapters = pd.read_csv('./csv_producao/capitulos_all.csv',
                             header=0, dtype='str')
    dfchapters_uniq = pd.read_csv('./csv_producao/capitulos_uniq.csv',
                                  header=0, dtype='str')
    dfadvise = pd.read_csv('./csv_producao/orientacoes_all.csv',
                           header=0, dtype='str')

    # filtrando o ano
    # projetos ALL
    dfppe_all['YEAR_INI'] = dfppe_all['YEAR_INI'].replace('VAZIO', -99)
    ppenum99 = dfppe_all[dfppe_all['YEAR_INI'] == -99].reset_index(drop=True)
    if len(ppenum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(ppenum99)) + 'projetos sem ano inicial')
        print('------------------------------------------------------------')
    dfppe_all['YEAR_INI'] = dfppe_all['YEAR_INI'].apply(ff)
    dfppe_all = dfppe_all[(dfppe_all['YEAR_INI'] >= yyi)]
    # projetos unique
    dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].replace('VAZIO', -99)
    ppenum99 = dfppe_uniq[dfppe_uniq['YEAR_INI'] == -99].reset_index(drop=True)
    if len(ppenum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(ppenum99)) + 'projetos sem ano inicial')
        print('------------------------------------------------------------')
    dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].apply(ff)
    dfppe_uniq = dfppe_uniq[(dfppe_uniq['YEAR_INI'] >= yyi)]

    # ------------------------------------------------------------
    # periodicos
    dfpaper['YEAR'] = dfpaper['YEAR'].replace('VAZIO', -99)
    dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].replace('VAZIO', -99)
    pernum99 = dfpaper[dfpaper['YEAR'] == -99].reset_index(drop=True)
    if len(pernum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(pernum99)) +
              'artigos sem ano de publicacao')
        print('------------------------------------------------------------')
    dfpaper['YEAR'] = dfpaper['YEAR'].apply(ff)
    dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].apply(ff)
    dfpaper = dfpaper[(dfpaper['YEAR'] >= yyi) & (dfpaper['YEAR'] <= yyf)]
    dfpaper_uniq = dfpaper_uniq[(dfpaper_uniq['YEAR']
                                 >= yyi) & (dfpaper_uniq['YEAR'] <= yyf)]

    # ------------------------------------------------------------
    # livros
    dfbooks['YEAR'] = dfbooks['YEAR'].replace('VAZIO', -99)
    dfbooks_uniq['YEAR'] = dfbooks_uniq['YEAR'].replace('VAZIO', -99)
    booknum99 = dfbooks[dfbooks['YEAR'] == -99].reset_index(drop=True)
    if len(booknum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(booknum99)) +
              ' livros sem ano de publicacao')
        print('------------------------------------------------------------')
    dfbooks['YEAR'] = dfbooks['YEAR'].apply(ff)
    dfbooks_uniq['YEAR'] = dfbooks_uniq['YEAR'].apply(ff)
    dfbooks = dfbooks[(dfbooks['YEAR'] >= yyi) & (dfbooks['YEAR'] <= yyf)]
    dfbooks_uniq = dfbooks_uniq[(dfbooks_uniq['YEAR']
                                 >= yyi) & (dfbooks_uniq['YEAR'] <=
                                            yyf)]

    # ------------------------------------------------------------
    # capitulos
    dfchapters['YEAR'] = dfchapters['YEAR'].replace('VAZIO', -99)
    dfchapters_uniq['YEAR'] = dfchapters_uniq['YEAR'].replace('VAZIO', -99)
    chapnum99 = dfchapters[dfchapters['YEAR'] == -99].reset_index(drop=True)
    if len(chapnum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(chapnum99)) +
              ' capítulos sem ano de publicacao')
        print('------------------------------------------------------------')
    dfchapters['YEAR'] = dfchapters['YEAR'].apply(ff)
    dfchapters_uniq['YEAR'] = dfchapters_uniq['YEAR'].apply(ff)
    dfchapters = dfchapters[(dfchapters['YEAR'] >= yyi)
                            & (dfchapters['YEAR'] <= yyf)]
    dfchapters_uniq = dfchapters_uniq[(dfchapters_uniq['YEAR']
                                       >= yyi) & (dfchapters_uniq['YEAR'] <= yyf)]

    # ------------------------------------------------------------
    # orientacoes
    dfadvise['YEAR'] = dfadvise['YEAR'].replace('VAZIO', -99)
    chapnum99 = dfadvise[dfadvise['YEAR'] == -99].reset_index(drop=True)
    if len(chapnum99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: \n' + str(len(chapnum99)) +
              ' orientacoes sem ano de publicacao')
        print('------------------------------------------------------------')
    dfadvise['YEAR'] = dfadvise['YEAR'].apply(ff)
    dfadvise = dfadvise[(dfadvise['YEAR'] >= yyi)
                        & (dfadvise['YEAR'] <= yyf)]

    # ------------------------------------------------------------

    # ordenando por ano (crescente)
    dfppe_uniq_pesq = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'PESQUISA']
    dfppe_uniq_pesq = dfppe_uniq_pesq.sort_values(['YEAR_INI'])
    dfppe_uniq_ext = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'EXTENSAO']
    dfppe_uniq_ext = dfppe_uniq_ext.sort_values(['YEAR_INI'])
    dfpaper_uniq = dfpaper_uniq.sort_values(['YEAR'])
    dfbooks_uniq = dfbooks_uniq.sort_values(['YEAR'])
    dfchapters_uniq = dfchapters_uniq.sort_values(['YEAR'])
    dfadvise = dfadvise.sort_values(['YEAR'])
    # ------------------------------------------------------------
    # Descritivo do numero de proj pesq e ext // livros
    pp = dfppe_uniq_pesq.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
    pp_tot = pp['PROJ'].sum()
    ppe = dfppe_uniq_ext.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
    ppe_tot = ppe['PROJ'].sum()
    liv = dfbooks_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    liv_tot = liv['TITLE'].sum()
    chap = dfchapters_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    chap_tot = chap['TITLE'].sum()
    advi = dfadvise.groupby(['NATURE'])['STUDENT'].size().reset_index()
    advi_tot = advi['STUDENT'].sum()
    advi.columns = ['NATUREZA', 'QTD']

    # ------------------------------------------------------------
    # GRAFICO artig completo periodico
    acp = dfpaper_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    acp_tot = acp['TITLE'].sum()
    plt.figure(figsize=(9, 5))
    plt.bar(x=acp['YEAR'], height=acp['TITLE'])
    plt.title('Publicações %i - %i' % (yyi, yyf))
    plt.xticks(np.arange(yyi, yyf + 1, 1))
    plt.xlabel('Ano')
    plt.ylabel('Número de publicações')
    plt.tight_layout()
    plt.savefig('./relatorio/figures/period_dep_year.png')
    # plt.show()
    # ------------------------------------------------------------
    # GRAFICO artig completo periodico por qualis
    acpq = dfpaper_uniq.groupby(['QUALIS'])['TITLE'].size().reset_index()
    # acpq
    plt.figure(figsize=(9, 5))
    plt.bar(x=acpq['QUALIS'], height=acpq['TITLE'])
    plt.title('Publicações %i - %i' % (yyi, yyf))
    plt.xlabel('Qualis')
    plt.ylabel('Número de publicações')
    plt.tight_layout()
    plt.savefig('./relatorio/figures/period_year_qualis.png')
    # plt.show()
    # ------------------------------------------------------------
    # GRAFICO livros
    livp = dfbooks_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    plt.figure(figsize=(9, 5))
    plt.bar(x=livp['YEAR'], height=livp['TITLE'])
    plt.title('Livros  %i - %i' % (yyi, yyf))
    plt.xticks(np.arange(yyi, yyf + 1, 1))
    plt.xlabel('Ano')
    plt.ylabel('Número de livros')
    plt.yticks(np.arange(0, livp['TITLE'].max() + 10, 5))
    plt.tight_layout()
    plt.savefig('./relatorio/figures/livros_dep_year.png')
    # plt.show()
    # ------------------------------------------------------------
    # GRAFICO capitulos
    capp = dfchapters_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    plt.figure(figsize=(9, 5))
    plt.bar(x=capp['YEAR'], height=capp['TITLE'])
    plt.title('Capítulos %i - %i' % (yyi, yyf))
    plt.xticks(np.arange(yyi, yyf + 1, 1))
    plt.xlabel('Ano')
    plt.ylabel('Número de capítulos')
    plt.yticks(np.arange(0, capp['TITLE'].max() + 10, 5))
    plt.tight_layout()
    plt.savefig('./relatorio/figures/capitulos_dep_year.png')
    # plt.show()

    # INICIANDO o html
    htmlfile = open('./relatorio/relatorio_producao.html', 'w')
    htmlfile.write('<!DOCTYPE html> \n ')
    htmlfile.write('<head> \n ')
    htmlfile.write(
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  \n')
    htmlfile.write(' <title>lucyLattes Relatorio</title> \n')
    htmlfile.write(
        '<link rel="stylesheet" href="./css/GITGUB.css" type="text/css" /> \n </head> \n')
    htmlfile.write('</head> \n ')
    htmlfile.write('<body> \n')
    # quick sumario
    htmlfile.write('<h0 class="title">Relatório de Produção</h0> \n <br>\n')
    htmlfile.write('<small>Gerado por <i>lucyLattes.py</i>' + ' ' +
                   '<a href="https://github.com/rafatieppo/lucyLattes">https://github.com/rafatieppo/lucyLattes</a></small> \n <br> \n')
    htmlfile.write(
        '<a href="https://doi.org/10.5281/zenodo.2591748"> <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2591748.svg" alt="DOI"> </a>')
    htmlfile.write('<h1 class="title">Sumário</h1> \n')
    htmlfile.write('<a href="#team">Equipe</a> \n <br>')
    htmlfile.write('<a href="#resprod">Resumo da produção</a> \n <br>')
    htmlfile.write('<a href="#projexte">Projetos de extensão</a> \n <br>')
    htmlfile.write('<a href="#projpesq">Projetos de pesquisa</a> \n <br>')
    htmlfile.write('<a href="#pubbookchap">Livros e capítulos</a> \n <br>')
    htmlfile.write('<a href="#pubperiod">Artigos em periódicos</a> \n <br>')
    htmlfile.write(
        '<a href="#prodporpesq">Extrato de periódicos por integrante</a> \n <br>')
    # Equipe
    htmlfile.write('<a name="team"></a>' + '\n \n')
    htmlfile.write('<h1 class="title">Equipe</h1> \n')
    # Descricao de cada pesquisador
    # df com nome completo, sobrenome e id
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    # passando ID para string, para poder comparar com dfpaper
    # dfpaper['ID'] = dfpaper['ID'].apply(ss)
    # dffullname['ID'] = dffullname['ID'].apply(ss)
    # dfpaper = pd.merge(dfpaper, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    for idd in range(len(dffullname)):
        htmlfile.write('<hr>')
        htmlfile.write('<b>Nome: </b>')
        htmlfile.write(dffullname.iloc[idd, 1])
        htmlfile.write('<br>')
        htmlfile.write('<b>Nascimento: </b>')
        htmlfile.write(dffullname.iloc[idd, 4])
        htmlfile.write(' - ')
        htmlfile.write(str(dffullname.iloc[idd, 5]))
        htmlfile.write('<br>')
        htmlfile.write('<b>Resumo: </b>')
        htmlfile.write(str(dffullname.iloc[idd, 6]))
        htmlfile.write('<p>')
        htmlfile.write('<b>Lattes: </b>')
        latteslink = 'http://lattes.cnpq.br/' + str(dffullname.iloc[idd, 0])
        htmlfile.write('<a href="' + latteslink + '">' + latteslink + '</a>')
        # resumo da produção projetos, periodicos
    htmlfile.write('<hr> \n')
    htmlfile.write('<a name="resprod"></a>' + '\n \n')
    htmlfile.write('<h1>Resumo da Produção</h1> \n')
    htmlfile.write('Período avaliado: ' + str(int(yyi)) +
                   ' - ' + str(int(yyf)) + '\n <br> \n')
    htmlfile.write('Número de membros na equipe: ' +
                   (str(len(dffullname)) + '\n <br> \n'))
    htmlfile.write('Número de projetos de extensão: ' +
                   (str(ppe_tot) + '\n <br> \n'))
    htmlfile.write('Número de projetos de pesquisa: ' +
                   (str(pp_tot) + '\n <br> \n'))
    htmlfile.write('Livros publicados: ' +
                   (str(liv_tot) + '\n <br> \n'))
    htmlfile.write('Capítulos publicados: ' +
                   (str(chap_tot) + '\n <br> \n'))
    htmlfile.write('Artigos completos publicados em periódicos: ' +
                   (str(acp_tot) + '\n <br> <br> \n'))
    htmlfile.write('Orientações:' + '\n <br>')
    for oo in range(len(advi)):
        htmlfile.write(str(advi.iloc[oo, 0]).lower() +
                       ': ' + str(advi.iloc[oo, 1]) + '\n <br>')
    # htmlfile.write(str(advi))
    htmlfile.write('\n <hr> \n \n')
    # Projetos de Extensao do Grupo
    htmlfile.write('<a name="projexte"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de extensão</h1> \n')
    htmlfile.write('<ol class="custom-counter">')
    for idd in range(len(dfppe_uniq_ext)):
        proj = dfppe_uniq_ext.iloc[idd, 0]
        proj_yi = dfppe_uniq_ext.iloc[idd, 1]
        proj_yf = dfppe_uniq_ext.iloc[idd, 2]
        proj_au = dfppe_uniq_ext.iloc[idd, 4]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                       str(proj_yi) + '</u>.' + ' fim: <u> ' + str(proj_yf)
                       + '.</u> ' + '<i>' + proj_au + '</i>.')
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
    htmlfile.write('</ol>')
    # Projetos de Pesquisa
    htmlfile.write('<a name="projpesq"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de pesquisa</h1> \n')
    htmlfile.write('<ol class="custom-counter">')
    for idd in range(len(dfppe_uniq_pesq)):
        proj = dfppe_uniq_pesq.iloc[idd, 0]
        proj_yi = dfppe_uniq_pesq.iloc[idd, 1]
        proj_yf = dfppe_uniq_pesq.iloc[idd, 2]
        proj_au = dfppe_uniq_pesq.iloc[idd, 4]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                       str(proj_yi) + '</u>' + ' fim: <u> ' + str(proj_yf)
                       + '.</u> ' + '<i>' + proj_au + '</i>.')
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
    htmlfile.write('</ol>')
    # Publicacao livros e capitulos
    htmlfile.write('<a name="pubbookchap"></a>' + '\n \n')
    htmlfile.write('<h1>Publicação de livros e capítulos</h1> \n')
    # Grafico de livros publicados por ano
    htmlfile.write('<h2>Produção de livros por ano</h2> \n')
    htmlfile.write('<figure> \n')
    htmlfile.write('<img src="./figures/livros_dep_year.png" alt="" ')
    htmlfile.write('width = "560" height = "auto" >\n')
    htmlfile.write('<figcaption>Número de livros por ano.</figcaption>\n')
    htmlfile.write('</figure> \n')
    htmlfile.write('\n <hr> \n \n')
    # Grafico de capitulos publicados por ano
    htmlfile.write('<h2>Produção de capítulos por ano</h2> \n')
    htmlfile.write('<figure> \n')
    htmlfile.write('<img src="./figures/capitulos_dep_year.png" alt="" ')
    htmlfile.write('width = "560" height = "auto" >\n')
    htmlfile.write('<figcaption>Número de capítulos por ano.</figcaption>\n')
    htmlfile.write('</figure> \n')
    htmlfile.write('\n <hr> \n \n')

    # Resumo da producao de livros do GRUPO
    gg = dfbooks
    gg['YEAR'] = gg['YEAR'].apply(iint)
    gg = gg.groupby(['FULL_NAME', 'YEAR'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    gg.fillna(0, inplace=True)
    gg['TOTAL'] = gg.sum(axis=1)
    ggt = (tabulate(gg, headers="keys", tablefmt='html'))
    # print(ggt)
    htmlfile.write(
        '<h2> Resumo da produção de livros do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
    htmlfile.write(ggt + '\n <br> \n <br> \n')

    if len(booknum99) >= 1:
        htmlfile.write('<b style="color:red;"> ATENCAO:\n ' + str(len(booknum99)) +
                       'projetos sem ano inicial</b>\n')
        for tt in range(len(booknum99)):
            htmlfile.write('\n <li>' + booknum99.iloc[tt, 0] + '\n </li>')
        htmlfile.write('<hr> \n')

    # Resumo da producao de capitulos do GRUPO
    gg = dfchapters
    gg['YEAR'] = gg['YEAR'].apply(iint)
    gg = gg.groupby(['FULL_NAME', 'YEAR'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    gg.fillna(0, inplace=True)
    gg['TOTAL'] = gg.sum(axis=1)
    ggt = (tabulate(gg, headers="keys", tablefmt='html'))
    # print(ggt)
    htmlfile.write(
        '<h2> Resumo da produção de capítulos do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
    htmlfile.write(ggt + '\n <br> \n <br> \n')

    if len(chapnum99) >= 1:
        htmlfile.write('<b style="color:red;"> ATENCAO:\n ' + str(len(chapnum99)) +
                       'projetos sem ano inicial</b>\n')
        for tt in range(len(chapnum99)):
            htmlfile.write('\n <li>' + chapnum99.iloc[tt, 0] + '\n </li>')
        htmlfile.write('<hr> \n')

    # Publicacao em periodicos
    htmlfile.write('<a name="pubperiod"></a>' + '\n \n')
    htmlfile.write('<h1>Publicação em periódicos</h1> \n')
    # Grafico de producao de periodicos por ano
    htmlfile.write('<h2>Produção de periódicos por ano</h2> \n')
    htmlfile.write('<figure> \n')
    htmlfile.write('<img src="./figures/period_dep_year.png" alt="" ')
    htmlfile.write('width = "560" height = "auto" >\n')
    htmlfile.write('<figcaption>Número de publicações por ano.</figcaption>\n')
    htmlfile.write('</figure> \n')
    htmlfile.write('\n <hr> \n \n')
    # Grafico de producao por qualis
    htmlfile.write('<h2>Produção de periódicos por qualis</h2> \n')
    htmlfile.write('<figure> \n')
    htmlfile.write('<img src="./figures/period_year_qualis.png" alt="" ')
    htmlfile.write('width = "560" height = "auto" >\n')
    htmlfile.write(
        '<figcaption>Publicações de periódicos por qualis.</figcaption>\n')
    htmlfile.write('</figure> \n')
    htmlfile.write('\n <hr> \n \n')

    # Grafico de interacao no grupos APENAS em artigos
    htmlfile.write('<h2>Interação entre pesquisadores</h2> \n')
    htmlfile.write('<figure> \n')
    htmlfile.write('<img src="./figures/grapho.png" alt="" ')
    htmlfile.write('width = "560" height = "auto" >\n')
    htmlfile.write(
        '<figcaption>Grafo de colaboração entre pesquisadores apenas em artigos</figcaption>\n')
    htmlfile.write('</figure> \n')
    htmlfile.write('\n <br> \n \n')

    # Lista de profissionais sem interacao em periodicos
    dfnointer_period = pd.read_csv('./csv_producao/periodicos_nointer.csv',
                                   sep=',', header=0)
    if len(dfnointer_period) > 0:
        htmlfile.write(
            '<b><i>Não foi possível localizar interações em periódicos para os seguintes pesquisadores: </i></b><br> \n')
        htmlfile.write('<ul>')
        for i in range(len(dfnointer_period)):
            name = dfnointer_period.iloc[i, 0]
            htmlfile.write('<b style="color:gray;"> <li>' +
                           name + '</li> </b> \n')
        htmlfile.write('\n </ul> \n <br> \n')
    htmlfile.write('\n <hr> \n \n')

    # lista de publicacoes em periodicos
    htmlfile.write('<h2>Relação de artigos em periódicos</h2> \n')
    htmlfile.write('<ol class="custom-counter">')
    for idd in range(len(dfpaper_uniq)):
        pap = dfpaper_uniq.iloc[idd, 0]
        pap_yi = dfpaper_uniq.iloc[idd, 1]
        pap_jo = dfpaper_uniq.iloc[idd, 4]
        pap_qu = dfpaper_uniq.iloc[idd, 5]
        pap_au = dfpaper_uniq.iloc[idd, 7]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(pap) + '</u>. ano: <u>' + str(pap_yi) + '</u>, ' +
                       str(pap_jo) + ', <b>' + str(pap_qu) + '</b>. ' + str(pap_au))
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
    htmlfile.write('</ol> \n')
    # artig completo periodico por qualis para cada pesquisador
    htmlfile.write('<a name="prodporpesq"></a>' + '\n \n')
    htmlfile.write(
        '<h2>Produção individual de projetos e periódicos por ano e qualis ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n')
    for idd in range(len(dffullname)):
        # full name and link lattes
        htmlfile.write('<b><u>' + dffullname.iloc[idd, 1] + '</u></b> <br>')
        latteslink = 'http://lattes.cnpq.br/' + str(dffullname.iloc[idd, 0])
        htmlfile.write('- ' + '<a href="' + latteslink + '">' +
                       latteslink + '</a> ')
        lattesupda = str(dffullname.iloc[idd, 7])
        htmlfile.write('(atualizado em: ' +
                       lattesupda + ') <br> <br>')
        # projetos de pesquisa como coord
        pp_idd = dfppe_all[(dfppe_all['NATUREZA'] ==
                            'PESQUISA')].reset_index(drop=True)
        pp_idd = pp_idd[pp_idd['ID'] == str(
            dffullname.iloc[idd, 0])].reset_index(drop=True)
        # pp_idd = pp_idd[pp_idd['ID']
        #                 == str(1292986021348016)].reset_index(drop=True)
        count_pp_coord = 0
        lscount_pp_coord = []
        for ppi in range(len(pp_idd)):
            mm = pp_idd.iloc[ppi, 5]
            mm = mm.strip('[')
            mm = mm.strip(']')
            mm = mm.replace("'", "")
            mm = mm.split(',')
            mm = mm[0]
            mm = mm.strip()
            # print(mm)
            if mm == 'SIM':
                count_pp_coord = count_pp_coord + 1
                lscount_pp_coord.append(ppi)
        count_pp_integ = len(pp_idd) - count_pp_coord
        htmlfile.write(
            '<li>' + 'total de projetos de pesquisa como coordenador = ' + str(count_pp_coord) + '</li>\n')
        # for ppii in range(len(lscount_pp_coord)):
        #     projname = pp_idd.iloc[lscount_pp_coord[ppii], 0]
        #     htmlfile.write('-' + str(projname + '\n <br> \n'))
        htmlfile.write(
            '<li>' + 'total de projetos de pesquisa como integrante = ' + str(count_pp_integ) + '</li>\n')
        # ------------------------------------------------------------
        # orientacoes
        t = dfadvise[dfadvise['ID'] == dffullname.iloc[idd, 0]]
        t = t.groupby(['NATURE'])['STUDENT'].size().reset_index()
        htmlfile.write('<li>Orientações: \n <br> \n ' + '</li>\n')
        for oo in range(len(t)):
            htmlfile.write(str(t.iloc[oo, 0]).lower() +
                           ' = ' + str(t.iloc[oo, 1]) + '\n <br>\n')
        # ------------------------------------------------------------
        # livros
        t = dfbooks[dfbooks['ID'] == dffullname.iloc[idd, 0]]
        t = t.groupby(['FULL_NAME', 'YEAR'])[
            'TITLE'].size().reset_index(drop=False)
        tot = t['TITLE'].sum()
        htmlfile.write('<li>produção total de livros = ' +
                       str(tot) + '</li>\n')
        # capitulos
        t = dfchapters[dfchapters['ID'] == dffullname.iloc[idd, 0]]
        t = t.groupby(['FULL_NAME', 'YEAR'])[
            'TITLE'].size().reset_index(drop=False)
        tot = t['TITLE'].sum()
        # print(tot)
        htmlfile.write('<li>produção total de capítulos = ' +
                       str(tot) + '</li>\n')
        # artigos
        b = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
        b = b.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        b = b.fillna(0)
        b.drop('FULL_NAME', axis=1, inplace=True)
        t = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
        t = t.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
            'TITLE'].size().reset_index(drop=False)
        tot = t['TITLE'].sum()
        # print(tot)
        htmlfile.write('<li>produção total de artigos = ' +
                       str(tot) + '</li>\n <br> \n')
        # print(b.head())
        # print(tabulate(b.head(), headers="keys", tablefmt='markdown'))
        mm = (tabulate(b, headers="keys", tablefmt='html'))
        htmlfile.write(str(mm))
        htmlfile.write('\n <hr> \n')
        # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Tabela de orientacoes
    advgg = dfadvise
    advgg['NATURE'] = advgg['NATURE'].str.replace('-', ' ')
    advgg['NATURE'] = advgg['NATURE'].str.replace('_', ' ')
    advgg = advgg.groupby(['FULL_NAME', 'NATURE'])[
        'STUDENT'].size().unstack().reset_index(drop=False)
    advgg.fillna(0, inplace=True)
    advgg['TOTAL'] = advgg.sum(axis=1)
    advggt = (tabulate(advgg, headers="keys", tablefmt='html'))
    htmlfile.write(
        '<h2> Resumo de orientações do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
    htmlfile.write(advggt + ' \n')
    htmlfile.write('<i>Possibilidade da contabilização de co-orientação.<i>')

    # ------------------------------------------------------------
    # Tabela de producao em periodicos
    gg = dfpaper
    gg = gg.groupby(['FULL_NAME', 'QUALIS'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    gg.fillna(0, inplace=True)
    gg['TOTAL'] = gg.sum(axis=1)
    ggt = (tabulate(gg, headers="keys", tablefmt='html'))
    # print(ggt)
    htmlfile.write(
        '<h2> Resumo da produção de artigos em periódicos do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
    htmlfile.write(ggt + '\n <br> \n <br> \n')

    if len(ppenum99) >= 1:
        htmlfile.write('<b style="color:red;"> ATENCAO:\n ' + str(len(ppenum99)) +
                       'projetos sem ano inicial</b>\n')
        for tt in range(len(ppenum99)):
            htmlfile.write('\n <li>' + ppenum99.iloc[tt, 0] + '\n </li>')
        htmlfile.write('<hr> \n')
    if len(pernum99) >= 1:
        htmlfile.write('b style="color:red;"> ATENCAO:\n ' + str(len(pernum99)) +
                       'periódicos sem ano</n>\n')
        for tt in range(len(pernum99)):
            htmlfile.write('\n <li>' + pernum99.iloc[tt, 0] + '\n </li>')
        htmlfile.write('<hr> \n')

    htmlfile.write('<b>AVISOS</b>:\n ')
    htmlfile.write(
        '<li>Arquivo para classificacao qualis utilizado: <code>' + qualqualis + '</code >')
    htmlfile.write('<li>Este programa é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU. Verifique o arquivo LICENSE.txt</li> \n')
    htmlfile.write(
        '<li>Os resultados estão sujeitos a falhas devido a inconsistencias no preenchimento dos CVs Lattes</li>\n')
    htmlfile.write(
        '<li>Em caso de erro do script abra um chamado no <a href="https://github.com/rafatieppo/lucyLattes">repositório lucyLattes</a>  </li>\n')
    htmlfile.write(
        '<li>O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta relatorio</li>\n')
    htmlfile.write(
        '<li>O arquivo relatorio_producao.html foi gerado na pasta relatorio</li>\n')
    htmlfile.write(
        '<li>Caso precise citar é possível usar o DOI: 10.5281/zenodo.2591748</li>\n')
    htmlfile.write('<br> <br> <br>')
    htmlfile.write('<footer> \n')
    htmlfile.write(
        'Relatório gerado por lucyLattes v1.0. Os resultados estão sujeitos a falhas devido a inconsistências no preenchimento dos CVs Lattes.')
    htmlfile.write('\n <br>')
    htmlfile.write('Para maiores informações acesse o repositório: ')
    htmlfile.write(
        '<a href="https://github.com/rafatieppo/lucyLattes">https://github.com/rafatieppo/lucyLattes</a> \n <br> \n')
    htmlfile.write('</footer> \n')
    htmlfile.close()
    # ------------------------------------------------------------
    # arquivo csv com autores producao ano qualis
    acpq_pesq = dfpaper_uniq.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    acpq_pesq = acpq_pesq.fillna(0)
    acpq_pesq.to_csv('./relatorio/extrato_periodico_autorqualis.csv')
    print('------------------------------------------------------------')
    print('AVISOS')
    print('------------------------------------------------------------')
    print('- Arquivo para classificacao qualis utilizado: ' + qualqualis)
    print('- Este programa é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU. Verifique o arquivo LICENSE.txt ')
    print('- Os resultados estão sujeitos a falhas devido a inconsistencias no preenchimento dos CVs Lattes')
    print('- Em caso de erro do script abra um chamado em https://github.com/rafatieppo/lucyLattes')
    print('- O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta relatorio')
    print('- O arquivo relatorio_producao.html foi gerado na pasta relatorio')
    print('- Caso precise citar é possível usar o DOI: 10.5281/zenodo.2591748')
    print('------------------------------------------------------------')
