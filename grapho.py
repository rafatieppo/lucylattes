# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import glob
import re

import matplotlib.pyplot as plt
import networkx as nx


# ------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------
from readidlist import readIdList
from extrafuns import *
# ------------------------------------------------------------


def getgrapho():
    # lendo a lista dos IDs e nome dos pesquisadores
    df_idlist = readIdList()
    # df_idlist['ID_LATTES'] = df_idlist['ID_LATTES'].apply(ss)
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    yyi = config_file.readlines()[5].split(':')[1]
    yyi = yyi.rstrip('\n')
    yyi = yyi.strip(' ')
    yyi = float(yyi)
    config_file.close()
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
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
    # paper uniq
    dfpaper['ID'] = dfpaper['ID'].apply(ss)
    dfpaper_uniq['ID'] = dfpaper_uniq['ID'].apply(ss)
    # filtrando o ano
    # projetos
    dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].replace('VAZIO', -99)
    num99 = dfppe_uniq[dfppe_uniq['YEAR_INI'] == -99]
    if len(num99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: ' + str(len(num99)) + 'projetos sem ano inicial')
        print('------------------------------------------------------------')
    dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].apply(ff)
    dfppe_uniq = dfppe_uniq[(dfppe_uniq['YEAR_INI'] >= yyi)]
    # ------------------------------------------------------------
    # periodicos
    dfpaper['YEAR'] = dfpaper['YEAR'].replace('VAZIO', -99)
    dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].replace('VAZIO', -99)
    num99 = dfpaper[dfpaper['YEAR'] == -99]
    if len(num99) >= 1:
        print('------------------------------------------------------------')
        print('ATENCAO: ' + str(len(num99)) + 'artigos sem ano de publicacao')
        print('------------------------------------------------------------')
    dfpaper['YEAR'] = dfpaper['YEAR'].apply(ff)
    dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].apply(ff)
    dfpaper = dfpaper[(dfpaper['YEAR'] >= yyi) & (dfpaper['YEAR'] <= yyf)]
    dfpaper_uniq = dfpaper_uniq[(dfpaper_uniq['YEAR']
                                 >= yyi) & (dfpaper_uniq['YEAR'] <= yyf)]
    # ------------------------------------------------------------
    # ordenando por ano (crescente)
    dfppe_uniq_pesq = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'PESQUISA']
    dfppe_uniq_pesq = dfppe_uniq_pesq.sort_values(['YEAR_INI'])
    dfppe_uniq_ext = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'EXTENSAO']
    dfppe_uniq_ext = dfppe_uniq_ext.sort_values(['YEAR_INI'])
    dfpaper = dfpaper.sort_values(['YEAR'])
    dfpaper_uniq = dfpaper_uniq.sort_values(['YEAR'])
    # ------------------------------------------------------------
    # carregando df com dados pessoais
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    # df com nome completo, sobrenome e id
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    # passando ID para string, para poder comparar com dfpaper
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dffullname = dffullname.reset_index(drop=True)
    # verificando a interacao de periodicos entre integrantes
    lsid = []
    lsid_tocompare = []
    lsinter_qtd = []
    for m in range(len(df_idlist)):
        idd = str(df_idlist.iloc[m, 0])
        lname = dffullname[dffullname['ID'] == idd]
        lname = lname.iloc[0, 1]
        lname = lname.upper()
        # lname = lname.split(';')
        # print(lname)
        dfids_tocompare = dffullname[dffullname['ID'] != str(idd)]
        for n in range(len(dfids_tocompare)):
            idd_tocompare = dfids_tocompare.iloc[n, 0]
            dd = dfpaper[dfpaper['ID'] == idd_tocompare]
            lsid.append(str(idd))
            lsid_tocompare.append(idd_tocompare)
            # DANGER ATTENTION FIX lname deve ser o nome completo
            # removendo caract desnecessarios
            interac = 0
            for o in range(len(dd)):
                authors = dd['AUTHOR'].iloc[o].upper()
                authors = authors.replace('[', '')
                authors = authors.replace(']', '')
                authors = authors.replace("'", '')
                authors = authors.split(',')
                # print(authors)
                for op in range(len(authors)):
                    # print(authors[op])
                    if len(authors[op]) > 0:
                        if authors[op][0] == ' ':
                            authors[op] = authors[op][1:]
                # interac = 0
                inpaper = list(set([lname]) & set(authors))
                if len(inpaper) >= 1:
                    interac = interac + 1
                    # print(interac)
                    # print(lname)
                    # print(authors)
            lsinter_qtd.append(interac)
    dfinterac = pd.DataFrame({'IDD': lsid,
                              'IDD_COMP': lsid_tocompare,
                              'WEIGHT': lsinter_qtd})
    # data frame para profissionais sem interacao em periodicos
    lsnointer_period = []
    for m in range(len(df_idlist)):
        aano = dfinterac[dfinterac['IDD'] == df_idlist.iloc[m, 0]]
        aasum = aano['WEIGHT'].sum()
        aano_a = dfinterac[dfinterac['IDD_COMP'] == df_idlist.iloc[m, 0]]
        aasum_a = aano_a['WEIGHT'].sum()
        if aasum == 0 and aasum_a == 0:
            nointer = dffullname[dffullname['ID'] ==
                                 df_idlist.iloc[m, 0]].reset_index(drop=True)
            nointer = nointer.iloc[0, 1]
            lsnointer_period.append(nointer)
    dfnointerac = pd.DataFrame({'NOME': lsnointer_period})
    dfnointerac.to_csv('./csv_producao/periodicos_nointer.csv',
                       index=False, sep=',')
    # DANGER ATTENTION
    # dfinterac.to_csv('test.csv', index=False)
    # eliminando linhas sem interacao
    indexremove = []
    for i in range(len(lsid)):
        if lsinter_qtd[i] == 0:
            indexremove.append(i)
    for index in sorted(indexremove, reverse=True):
        del lsid[index]
        del lsid_tocompare[index]
        del lsinter_qtd[index]
    # ------------------------------------------------------------
    # Grapho
    plt.figure(figsize=(12, 9.5))
    G = nx.Graph()
    for i in range(len(lsid)):
        G.add_edge(lsid[i],
                   lsid_tocompare[i],
                   weight=lsinter_qtd[0])
    pos = nx.spring_layout(G, 1.75)
    # colors for nodes
    colours = ['#5a7d9a', 'red', 'green', 'yellow',
               'gray', 'orange', 'blue', 'magenta',
               '#00555a', '#f7d560', 'cyan',    '#b6b129',
               '#a1dd72', '#d49acb', '#d4a69a', '#977e93',
               '#a3cc72', '#c60acb', '#d4b22a', '#255e53',
               '#77525a', '#c7d511', '#c4c22b', '#c9b329',
               '#c8dd22', '#f75acb', '#b1a40a', '#216693',
               '#b1cd32', '#b33acb', '#c9a32b', '#925e11',
               '#c5dd39', '#d04205', '#d8a82a', '#373e29']
    lsgroup_uniq = df_idlist['GROUP'].unique()
    dic_colours = {}
    for i in range(len(lsgroup_uniq)):
        dic_colours[lsgroup_uniq[i]] = colours[i]
    a = list(G.nodes())
    node_colours = []
    for i in range(len(a)):
        x = df_idlist[df_idlist['ID_LATTES'] == a[i]]
        x = x.iloc[0, 2]
        c = dic_colours[x]
        node_colours.append(c)
    # nodes
    nx.draw_networkx_nodes(G, pos,
                           node_size=400,
                           node_shape='o',
                           node_color=node_colours,
                           alpha=0.7)
    # labels
    nn = list(G.nodes)
    diclabel = {}
    for i in range(len(nn)):
        x = df_idlist[df_idlist['ID_LATTES'] == nn[i]]
        xid = x.iloc[0, 0]
        xname = x.iloc[0, 1]
        diclabel[str(xid)] = xname
    # edges
    nx.draw_networkx_edges(G, pos,  # edgelist=lsinter_qtd,
                           width=1, edge_color='orange')
    # labels
    nx.draw_networkx_labels(G, pos, labels=diclabel, font_size=16,
                            font_family='sans-serif')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('./relatorio/figures/grapho.png')
    # plt.show()

# ------------------------------------------------------------
# ------------------------------------------------------------
# Com pesos
# ------------------------------------------------------------

# G = nx.Graph()
# for i in range(len(lsid)):
#     G.add_edge(lsid[i], lsid_tocompare[i], weight=lsinter_qtd[0])
# # elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 3]
# # esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 3]
# pos = nx.spring_layout(G)  # positions for all nodes
# # nodes
# nx.draw_networkx_nodes(G, pos,
#                        node_size=400,
#                        node_shape='o',
#                        node_color=node_colours)
# # label = lsinter_qtd)
# # edges
# nx.draw_networkx_edges(G, pos,  # edgelist=lsinter_qtd,
#                        width=1, edge_color='orange')
# # nx.draw_networkx_edges(G, pos, edgelist=elarge,
# #                       width=1, edge_color='orange')
# # nx.draw_networkx_edges(G, pos, edgelist=esmall,
# #                       width=1, arrowsize=30, alpha=0.5,
# #                       edge_color='b', style='dashed')
# # labels
# nx.draw_networkx_labels(G, pos, labels=diclabel,
#                         font_size=14, font_family='sans-serif')
# plt.axis('off')
# plt.show()
# ------------------------------------------------------------
