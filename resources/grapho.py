"""Generate a grapho from papers interactions among researchers."""

import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from resources.support_functions import yearlimit_forfilter
from resources.support_functions import writecsv_from_lspdseries


def grapho_paper():
    """Generate a grapho from papers interactions among researchers."""
    lsyear_limits = yearlimit_forfilter()
    dffullname = pd.read_csv('./csv_producao/fullname_all.csv',
                             header=0, dtype='str')
    dfpaper = pd.read_csv('./csv_producao/papers_all.csv',
                          header=0, dtype='str')
    # dfpaper_uniq = pd.read_csv('./csv_producao/papers_uniq.csv',
    #                            header=0, dtype='str')
    # create a df for idlist with researchres identification
    dfidlist = dffullname.loc[:, ['ID', 'FULL_NAME', 'CITADO']].copy()
    dfidlist['NICKNAME'] = [str(xx.split(' ')[-1] +
                                xx.split(' ')[0][0:4])
                            for xx in dfidlist['FULL_NAME'].to_list()]

    # change year to integer and filter by year period
    dfpaper['YEAR'] = [int(yy) for yy in dfpaper['YEAR'].to_list()]
    dfpaper = dfpaper[(dfpaper['YEAR'] >= lsyear_limits[0]) &
                      (dfpaper['YEAR'] <= lsyear_limits[1])]

    # check interaction among reserchers only for papers
    lsid = []
    lsid_tocompare = []
    lsinteract_amount = []
    for idx in range(len(dfidlist)):
        id = str(dfidlist['ID'].iloc[idx])
        citation_mode = dfidlist['CITADO'].iloc[idx]
        citation_mode = citation_mode.upper()
        citation_mode = citation_mode.split(';')
        citation_mode.append(dfidlist['FULL_NAME'].iloc[idx].upper())
        dfids_tocompare = dfidlist[dfidlist['ID'] != str(id)]
        for idy in range(len(dfids_tocompare)):
            id_tocompare = dfids_tocompare['ID'].iloc[idy]
            dfpapers_tocompare = dfpaper[
                dfpaper['ID'] == id_tocompare].reset_index(drop=True)
            # fill list with id and id_tocompare
            lsid.append(id)
            lsid_tocompare.append(id_tocompare)
            # comparing citation_mode with authors
            interaction = 0
            for idz in range(len(dfpapers_tocompare)):
                lsauthors = dfpapers_tocompare['AUTHOR'].iloc[idz]
                lsauthors = re.sub(r'(\[|\])', '', lsauthors)
                lsauthors = lsauthors.upper()
                lsauthors = lsauthors.split("'")
                lsauthors_clean = []
                [lsauthors_clean.append(xx) for xx in lsauthors if len(xx) > 5]
                inpaper = list(set(citation_mode) & set(lsauthors))
                if len(inpaper) >= 1:
                    interaction += 1
                    # print(id, id_tocompare, inpaper)
            lsinteract_amount.append(interaction)

    # create a df with iteractions
    dfinteract = pd.DataFrame({'ID': lsid,
                               'ID_COMPER': lsid_tocompare,
                               'INTERACTION': lsinteract_amount})
    # drop duplicates permutatios
    dfinteract['INDEXX'] = np.repeat(-99, len(dfinteract))
    dfinteract.reset_index(inplace=True, drop=True)
    dfinteract_clean = dfinteract.copy()
    for idx in range(len(dfinteract_clean)):
        # each df_ is a filter for a reverse pair id and id_comper
        df_c = dfinteract_clean[
            (dfinteract_clean['ID'] == dfinteract_clean['ID_COMPER'].iloc[idx]) &
            (dfinteract_clean['ID_COMPER'] == dfinteract_clean['ID'].iloc[idx])]
        index_c = df_c.index[0]
        if dfinteract_clean.loc[idx, 'INDEXX'] == -99:
            dfinteract_clean.loc[idx, 'INDEXX'] = idx
        if dfinteract_clean.loc[index_c, 'INDEXX'] == -99:
            dfinteract_clean.loc[index_c, 'INDEXX'] = idx
    dfinteract_clean.sort_values(by=['INDEXX', 'INTERACTION'],
                                 ascending=False, inplace=True)
    dfinteract_clean.reset_index(inplace=True, drop=True)
    dfinteract_clean.drop_duplicates(['INDEXX'], inplace=True)
    dfinteract_clean.reset_index(inplace=True, drop=True)

    # create a df for id with and with no interactions
    lsid_with_interac = []
    lsid_withno_interac = []
    for idx in range(len(dffullname)):
        df_c = dfinteract_clean[dfinteract_clean['ID']
                                == dffullname['ID'].iloc[idx]]
        df_d = dfinteract_clean[dfinteract_clean['ID_COMPER']
                                == dffullname['ID'].iloc[idx]]
        if df_c['INTERACTION'].sum() + df_d['INTERACTION'].sum() == 0:
            lsid_withno_interac.append(dffullname.iloc[idx])
        else:
            lsid_with_interac.append(dffullname.iloc[idx])

    writecsv_from_lspdseries(
        lsid_with_interac,
        './csv_producao/' + 'papers_with_interact.csv',
        'There is no researchers with interactions')
    dfresch_withno_interact = writecsv_from_lspdseries(
        lsid_withno_interac,
        './csv_producao/' + 'papers_withno_interact.csv',
        'All researchers have one interaction at least in papers')

    # plot interactions
    dfgrapho = dfinteract_clean.copy()  # there with and withno interc
    # if len(dfresch_withno_interact['ID']) >= 1:
    #     lsid_todrop = dfresch_withno_interact['ID'].to_list()
    #     lsrow_todrop = []
    #     for idx in range(len(dfgrapho)):
    #         if len(list(set(
    #                 [dfgrapho['ID'].iloc[idx],
    #                  dfgrapho['ID_COMPER'].iloc[idx]]) & set(lsid_todrop))) >= 1:
    #             lsrow_todrop.append(idx)
    #         dfgrapho.drop(lsrow_todrop, inplace=True)
    #         dfgrapho.reset_index(drop=True, inplace=True)
    # drop row with 0 interactions, maybe threre is no interc between rserc
    dfgrapho = dfgrapho[dfgrapho['INTERACTION'] != 0]
    dfgrapho.reset_index(drop=True, inplace=True)

    plt.figure(figsize=(14, 9.5), dpi=200)
    G = nx.Graph()
    for idx in range(len(dfgrapho)):
        G.add_edge(dfgrapho['ID'].iloc[idx],
                   dfgrapho['ID_COMPER'].iloc[idx],
                   weight=dfgrapho['INTERACTION'].iloc[idx])
    position = nx.spring_layout(G, 1.75)
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
    lsgroup_uniq = ['pg']
    dic_colours = {}
    for i in range(len(lsgroup_uniq)):
        dic_colours[lsgroup_uniq[i]] = colours[i]

    # nodes
    lsnodes = list(G.nodes())
    node_colours = []
    for i in range(len(lsnodes)):
        group = 'pg'
        color = dic_colours[group]
        node_colours.append(color)
    nx.draw_networkx_nodes(G, position, node_size=400, node_shape='o',
                           node_color=node_colours, alpha=0.7)
    # labels
    diclabel = {}
    for i in range(len(lsnodes)):
        x = dfidlist[dfidlist['ID'] == lsnodes[i]]
        xid = x.iloc[0, 0]
        nickname = x['NICKNAME'].iloc[0]
        diclabel[str(xid)] = nickname
    # edges
    nx.draw_networkx_edges(G, position,  # edgelist=lsinter_qtd,
                           width=1, edge_color='orange')
    # labels
    nx.draw_networkx_labels(G, position, labels=diclabel, font_size=16,
                            font_family='sans-serif')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('./relatorio/figures/grapho_paper.png')
    # plt.show()
