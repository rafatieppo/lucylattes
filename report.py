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
# style.available
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
    # ------------------------------------------------------------
    # importadando os data frames gerados pelo gettidy
    # ------------------------------------------------------------
    dfppe_uniq = pd.read_csv('./csv_producao/projetos_uniq.csv',
                             header=0)
    dfpaper = pd.read_csv('./csv_producao/periodicos_all.csv',
                          header=0)
    dfpaper_uniq = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                               header=0)
    # filtrando o ano
    # projetos
    dfppe_uniq = dfppe_uniq[(dfppe_uniq['YEAR_INI'] >= yyi)]
    # periodicos
    dfpaper = dfpaper[(dfpaper['YEAR'] >= yyi) & (dfpaper['YEAR'] <= yyf)]
    dfpaper_uniq = dfpaper_uniq[(dfpaper_uniq['YEAR']
                                 >= yyi) & (dfpaper_uniq['YEAR'] <= yyf)]
    # ------------------------------------------------------------
    # ordenando por ano (crescente)
    dfppe_uniq_pesq = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'PESQUISA']
    dfppe_uniq_pesq = dfppe_uniq_pesq.sort_values(['YEAR_INI'])
    dfppe_uniq_ext = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'EXTENSAO']
    dfppe_uniq_ext = dfppe_uniq_ext.sort_values(['YEAR_INI'])
    dfpaper_uniq = dfpaper_uniq.sort_values(['YEAR'])
    # ------------------------------------------------------------
    # Descritivo do numero de proj pesq e ext
    pp = dfppe_uniq_pesq.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
    pp_tot = pp['PROJ'].sum()
    ppe = dfppe_uniq_ext.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
    ppe_tot = ppe['PROJ'].sum()
    # ------------------------------------------------------------
    # GRAFICO artig completo periodico
    acp = dfpaper_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
    acp_tot = acp['TITLE'].sum()
    plt.figure(figsize=(9, 5))
    plt.bar(x=acp['YEAR'], height=acp['TITLE'])
    plt.title('Publicações %i - %i' % (yyi, yyf))
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
    # iniciando o html
    htmlfile = open('./relatorio/relatorio_producao.html', 'w')
    htmlfile.write('<!DOCTYPE html> \n ')
    htmlfile.write('<head> \n ')
    htmlfile.write(
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  \n')
    htmlfile.write(' <title>Lattes Relatorio</title> \n')
    htmlfile.write(
        '<link rel="stylesheet" href="./css/GITGUB.css" type="text/css" /> \n </head> \n')
    htmlfile.write('</head> \n ')
    htmlfile.write('<body> \n')
    # quick sumario
    htmlfile.write('<h1 class="title">Sumário</h1> \n')
    htmlfile.write('<a href="#team">Equipe</a> \n <br>')
    htmlfile.write('<a href="#resprod">Resumo da produção</a> \n <br>')
    htmlfile.write('<a href="#projexte">Projetos de extensão</a> \n <br>')
    htmlfile.write('<a href="#projpesq">Projetos de pesquisa</a> \n <br>')
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
        a = pd.read_csv(lscsv_fullname[i], header=0)
        dffullname = dffullname.append(a, ignore_index=False)
    # passando ID para string, para poder comparar com dfpaper
    dfpaper['ID'] = dfpaper['ID'].apply(ss)
    dffullname['ID'] = dffullname['ID'].apply(ss)
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
    htmlfile.write('Número de projetos de extensão: ' +
                   (str(ppe_tot) + '\n <br> \n'))
    htmlfile.write('Número de projetos de pesquisa: ' +
                   (str(pp_tot) + '\n <br> \n'))
    htmlfile.write('Artigos completos publicados em periódicos: ' +
                   (str(acp_tot) + '\n <br> \n'))
    htmlfile.write('\n <hr> \n \n')
    # Projetos de Extensao do Grupo
    htmlfile.write('<a name="projexte"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de extensão</h1> \n')
    for idd in range(len(dfppe_uniq_ext)):
        proj = dfppe_uniq_ext.iloc[idd, 0]
        proj_yi = dfppe_uniq_ext.iloc[idd, 1]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                       str(proj_yi) + '</u>')
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
    # Projetos de Pesquisa
    htmlfile.write('<a name="projpesq"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de pesquisa</h1> \n')
    for idd in range(len(dfppe_uniq_pesq)):
        proj = dfppe_uniq_pesq.iloc[idd, 0]
        proj_yi = dfppe_uniq_pesq.iloc[idd, 1]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                       str(proj_yi) + '</u>')
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
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
    htmlfile.write('\n <hr> \n \n')

    # lista de publicacoes em periodicos
    htmlfile.write('<h2>Relação de artigos em periódicos</h2> \n')
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
    # artig completo periodico por qualis para cada pesquisador
    htmlfile.write('<a name="prodporpesq"></a>' + '\n \n')
    htmlfile.write(
        '<h2>Produção individual de periódicos por ano e qualis</h2> \n')
    for idd in range(len(dffullname)):
        b = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
        b = b.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        b = b.fillna(0)
        b.drop('FULL_NAME', axis=1, inplace=True)
        t = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
        t = t.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
            'TITLE'].size().reset_index(drop=False)
        tot = t['TITLE'].sum()
        print(tot)
        htmlfile.write(dffullname.iloc[idd, 1])
        htmlfile.write(': produção total = ')
        htmlfile.write(str(tot))
        htmlfile.write('\n')
        # print(b.head())
        print(tabulate(b.head(), headers="keys", tablefmt='markdown'))
        mm = (tabulate(b, headers="keys", tablefmt='html'))
        htmlfile.write(str(mm))
        htmlfile.write('\n <hr> \n')
    htmlfile.write('<footer> \n')
    htmlfile.write(
        'Relatório gerado por scriptLattesRT v1.0. Os resultados estão sujeitos a falhas devido a inconsistências no preenchimento dos CVs Lattes.')
    htmlfile.write('\n <br>')
    htmlfile.write('Para maiores informações acesse o repositório: ')
    htmlfile.write(
        '<a href="https://github.com/rafatieppo/LATTES_SCRAPER">repositório scriptLattesRT </a> \n <br> \n')
    htmlfile.write('</footer> \n')
    htmlfile.close()
    # ------------------------------------------------------------
    # arquivo csv com autores producao ano qualis
    acpq_pesq = dfpaper_uniq.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    acpq_pesq = acpq_pesq.fillna(0)
    acpq_pesq.to_csv('./relatorio/extrato_periodico_autorqualis.csv')
    print('O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta relatorio')
