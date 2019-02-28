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
    df_idlist['ID_LATTES'] = df_idlist['ID_LATTES'].apply(ss)
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
    dfpaper['ID'] = dfpaper['ID'].apply(ss)
    dfpaper_uniq['ID'] = dfpaper_uniq['ID'].apply(ss)
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
    dfpaper = dfpaper.sort_values(['YEAR'])
    dfpaper_uniq = dfpaper_uniq.sort_values(['YEAR'])
    # ------------------------------------------------------------
    # carregando df com dados pessoais
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    # df com nome completo, sobrenome e id
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0)
        dffullname = dffullname.append(a, ignore_index=False)
    # passando ID para string, para poder comparar com dfpaper
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dffullname = dffullname.reset_index(drop=True)
    # verificando a interacao de periodicos entre integrantes
    lsid = []
    lsid_tocompare = []
    lsinter_qtd = []
    for m in range(len(df_idlist)):
        idd = df_idlist.iloc[m, 0]
        lname = dffullname[dffullname['ID'] == idd]
        lname = lname.iloc[0, 3]
        lname = lname.upper()
        lname = lname.split(';')
        # print(lname)
        dfids_tocompare = dffullname[dffullname['ID'] != str(idd)]
        for n in range(len(dfids_tocompare)):
            idd_tocompare = dfids_tocompare.iloc[n, 0]
            dd = dfpaper[dfpaper['ID'] == idd_tocompare]
            lsid.append(str(idd))
            lsid_tocompare.append(idd_tocompare)
            interac = 0
            for o in range(len(dd)):
                authors = dd.iloc[o, 7].upper()
                for p in range(len(lname)):
                    test = lname[p] in authors
                    if test == True:
                        interac = interac + 1
            lsinter_qtd.append(interac)
    dfinterac = pd.DataFrame({'IDD': lsid,
                              'IDD_COMP': lsid_tocompare,
                              'WEIGHT': lsinter_qtd})
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
    # labels para grapho
    lsid_uniq = np.unique(lsid)
    diclabel = {}
    for i in range(len(lsid_uniq)):
        x = df_idlist[df_idlist['ID_LATTES'] == lsid_uniq[i]]
        diclabel[lsid_uniq[i]] = x.iloc[0, 1]
    # ------------------------------------------------------------
    # Grapho
    plt.figure(figsize=(9, 5))
    G = nx.Graph()
    for i in range(len(lsid)):
        G.add_edge(lsid[i],
                   lsid_tocompare[i],
                   weight=lsinter_qtd[0])
    pos = nx.spring_layout(G)
    # colors for nodes
    colours = ['red', 'green', 'yellow', 'gray', 'orange', 'blue', 'magenta']
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
    # edges
    nx.draw_networkx_edges(G, pos,  # edgelist=lsinter_qtd,
                           width=1, edge_color='orange')
    # labels
    nx.draw_networkx_labels(G, pos, labels=diclabel, font_size=14,
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
