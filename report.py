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

# ------------------------------------------------------------
# Intervalo das produções ANOS
# ------------------------------------------------------------

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
# Funcoes
# ------------------------------------------------------------


def ss(x): return str(x)


# ------------------------------------------------------------
# Projetos de pesquisa e extensão
# ------------------------------------------------------------

# df com todos os periodicos
lscsv_ppe = glob.glob('./csv_producao/*_ppe.csv')
dfppe = pd.DataFrame()
lsid = []
for i in range(len(lscsv_ppe)):
    a = pd.read_csv(lscsv_ppe[i], header=0)
    dfppe = dfppe.append(a, ignore_index=False)
    id = lscsv_paper[i].split('_')[1].split('/')[1]
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

# retirando paper repetido, fica para o author com maior importancia
dfppe_uniq = dfppe.sort_values(['OR'])
dfppe_uniq.drop_duplicates(['PROJ'], inplace=True)


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

# ------------------------------------------------------------
# filtrando o ano

# periodicos
dfpaper = dfpaper[(dfpaper['YEAR'] >= yyi) & (dfpaper['YEAR'] <= yyf)]
dfpaper_uniq = dfpaper_uniq[(dfpaper_uniq['YEAR']
                             >= yyi) & (dfpaper_uniq['YEAR'] <= yyf)]
# projetos
dfppe_uniq = dfppe_uniq[(dfppe_uniq['YEAR_INI'] >= yyi)]

dfppe_uniq_pesq = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'PESQUISA']
dfppe_uniq_pesq = dfppe_uniq_pesq.sort_values(['YEAR_INI'])
dfppe_uniq_ext = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'EXTENSAO']
dfppe_uniq_ext = dfppe_uniq_ext.sort_values(['YEAR_INI'])
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
plt.show()

# ------------------------------------------------------------
# GRAFICO artig completo periodico por qualis
acpq = dfpaper_uniq.groupby(['QUALIS'])['TITLE'].size().reset_index()
acpq

plt.figure(figsize=(9, 5))
plt.bar(x=acpq['QUALIS'], height=acpq['TITLE'])
plt.title('Publicações %i - %i' % (yyi, yyf))
plt.xlabel('Qualis')
plt.ylabel('Número de publicações')
plt.tight_layout()
plt.savefig('./relatorio/figures/period_year_qualis.png')
plt.show()


# iniciando o html
htmlfile = open('./relatorio/relatorio_producao.html', 'w')
htmlfile.write('<!DOCTYPE html> \n ')
htmlfile.write('<head> \n ')
htmlfile.write(
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  \n')
htmlfile.write(' <title>Lattes Relatorio</title> \n')
htmlfile.write(
    '<link rel="stylesheet" href="./css/vignette.css" type="text/css" /> \n </head> \n')
htmlfile.write('</head> \n ')
htmlfile.write('<body> \n')
# Equipe
htmlfile.write('<h1 class="title">Equipe</h1> \n')
# Descricao de cada pesquisador
for idd in range(len(dffullname)):
    htmlfile.write('<hr>')
    htmlfile.write('<b>Nome: </b>')
    htmlfile.write(dffullname.iloc[idd, 1])
    htmlfile.write('<br>')
    htmlfile.write('<b>Nascimento: </b>')
    htmlfile.write(dffullname.iloc[idd, 3])
    htmlfile.write(' - ')
    htmlfile.write(str(dffullname.iloc[idd, 4]))
    htmlfile.write('<br>')
    htmlfile.write('<b>Resumo: </b>')
    htmlfile.write(dffullname.iloc[idd, 5])
    htmlfile.write('<p>')
    htmlfile.write('<b>Lattes: </b>')
    latteslink = 'http://lattes.cnpq.br/' + str(dffullname.iloc[idd, 0])
    htmlfile.write('<a href="' + latteslink + '">' + latteslink + '</a>')

# resumo da produção bibliográfica
htmlfile.write('<h2>Resumo da Produção</h2> \n')
htmlfile.write('Artigos completos publicados em periódicos: ')
htmlfile.write(str(acp_tot))
htmlfile.write('\n' + '\n <hr>')

# Projetos de Extensao do Grupo
htmlfile.write('<h2>Projetos de Extensão</h2> \n')
for idd in range(len(dfppe_uniq_ext)):
    proj = dfppe_uniq_ext.iloc[idd, 0]
    proj_yi = dfppe_uniq_ext.iloc[idd, 1]
    htmlfile.write('<li>' + '\n')
    htmlfile.write('<i>' + '\n')
    htmlfile.write(str(proj) + '. início: ' + str(proj_yi))
    htmlfile.write('</i>' + '\n')
    htmlfile.write('</li>' + '\n')
    htmlfile.write('<p>')

# Projetos de Pesquisa
htmlfile.write('<h2>Projetos de Pesquisa</h2> \n')
for idd in range(len(dfppe_uniq_pesq)):
    proj = dfppe_uniq_pesq.iloc[idd, 0]
    proj_yi = dfppe_uniq_pesq.iloc[idd, 1]
    htmlfile.write('<li>' + '\n')
    htmlfile.write('<i>' + '\n')
    htmlfile.write(str(proj) + '. início: ' + str(proj_yi))
    htmlfile.write('</i>' + '\n')
    htmlfile.write('</li>' + '\n')
    htmlfile.write('<p>')

# Grafico de producao de periodicos por ano
htmlfile.write('<h2>Produção de periódicos por ano</h2> \n')
htmlfile.write('<figure> \n')
htmlfile.write('<img src="./figures/period_dep_year.png" alt="" ')
htmlfile.write('width = "560" height = "auto" >\n </figure> \n')
htmlfile.write('\n <hr>')
# Graficoe de producao por e qualis
htmlfile.write('<h2>Produção de periódicos por qualis</h2> \n')
htmlfile.write('<figure> \n')
htmlfile.write('<img src="./figures/period_year_qualis.png" alt="" ')
htmlfile.write('width = "560" height = "auto" >\n </figure> \n')
htmlfile.write('\n <hr>')
# artig completo periodico por qualis para cada pesquisador
htmlfile.write(
    '<h2>Produção individual de periódicos por ano e qualis</h2> \n')
for idd in range(len(dffullname)):
    b = dfpaper_uniq[dfpaper_uniq['ID'] == dffullname.iloc[idd, 0]]
    b = b.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
        'TITLE'].size().unstack().reset_index(drop=False)
    b = b.fillna(0)
    b.drop('FULL_NAME', axis=1, inplace=True)
    t = dfpaper_uniq[dfpaper_uniq['ID'] == dffullname.iloc[idd, 0]]
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
    htmlfile.write('\n <hr>')
htmlfile.close()


# ------------------------------------------------------------

# arquivo csv com autores producao ano qualis
acpq_pesq = dfpaper_uniq.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
    'TITLE'].size().unstack().reset_index(drop=False)
acpq_pesq = acpq_pesq.fillna(0)
acpq_pesq.to_csv('./relatorio/extrato_periodico_autorqualis.csv')

print('O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta
      relatorio')
