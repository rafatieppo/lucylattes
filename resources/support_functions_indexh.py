"""Functions to aid in index h calculation."""

import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.ticker as mticker
# import numpy as np
import pandas as pd
style.use('fivethirtyeight')


def index_h(lsids, dfhwebsci, dffullname, txttosave):
    """Return index H for each researcher, df_websci can be all or unique."""
    ls_idlattes = []
    ls_hwebsci = []
    ls_publication_total = []
    ls_citation_total = []
    ls_citation_avr = []
    df_h = pd.DataFrame()
    for nid in range(len(lsids)):
        idlattes = lsids[nid]
        df_temp = dfhwebsci.query('ID_LATTES == @idlattes')
        ls_timewos = list(df_temp['Total Citations'])
        # condicao para testar se ha artigos citados
        if len(ls_timewos) == 0:
            publication_tot = 0
            citation_tot = 0
            citation_avr = 0
            hwos = 0
        else:
            # aproveitando para fazer o citacao media por item
            citation_tot = sum(ls_timewos)
            publication_tot = len(ls_timewos)
            citation_avr = citation_tot / publication_tot
            # o valor maximo do index H é o numero de trabalhos publicados
            hwos_max = len(ls_timewos)
            if hwos_max == 1:
                hwos = 1
            else:
                # ordem descrecente
                ls_timewos.sort(reverse=True)
                # hwos_freq frequencia do valor de hwos
                ncitat_hwos = 0
                hwos = hwos_max + 1
                while hwos > ncitat_hwos:
                    hwos -= 1
                    ncitat_hwos = len(
                        [xx for xx in ls_timewos if xx >= hwos])
        ls_idlattes.append(idlattes)
        ls_citation_total.append(citation_tot)
        ls_publication_total.append(publication_tot)
        ls_citation_avr.append(round(citation_avr, 2))
        # if citation_avr == 0:
        #     hwos = 0
        ls_hwebsci.append(hwos)

    # data frame saida
    df_h['ID_LATTES'] = ls_idlattes
    df_h['HWEBSCI'] = ls_hwebsci
    df_h['TOTAL_PUBLIC'] = ls_publication_total
    df_h['TOTAL_CITATION'] = ls_citation_total
    df_h['CITATION_AVR'] = ls_citation_avr

    # exportando csv da producao e index H de cada pesq
    df_h = pd.merge(df_h, dffullname,
                    left_on='ID_LATTES', right_on='ID')
    df_h = df_h.sort_values(['FULL_NAME'])
    df_h.reset_index(inplace=True, drop=True)

    pathtosave = './csv_producao_hindex/' + str(txttosave) + '.csv'
    df_h.to_csv(pathtosave, index=False, sep=',')

    # plot
    plt.figure(figsize=(10, 6))
    for ih in range(len(df_h)):
        plt.bar(x=df_h['NICKNAME'].iloc[ih],
                height=df_h['HWEBSCI'].iloc[ih])
    plt.title('Índice H base webofknowledge')
    plt.xlabel('Pesquisador', fontsize=15)
    plt.xticks(rotation=73)
    plt.ylabel('Índice H', fontsize=15)
    # plt.yticks(np.arange(0, tab['QTD'].max() + 3, 2))
    plt.gca().yaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.tight_layout()
    # plt.show()
    pathtosave = './relatorio/figures/' + str(txttosave) + '.png'
    plt.savefig(pathtosave)
    return df_h


def index_h_allgroup(dfhwebsci_uniq):
    """Return index H for group, df_websci is unique."""
    # h index for all group
    df_temp = dfhwebsci_uniq.copy()
    df_temp.reset_index(inplace=True, drop=True)
    ls_timewos = list(df_temp['Total Citations'])
    # condicao para testar se ha artigos citados
    if len(ls_timewos) == 0:
        citation_avr = 0
        hwos = 0
    else:
        # aproveitando para fazer o citacao media por item
        citation_tot = sum(ls_timewos)
        publication_tot = len(ls_timewos)
        citation_avr = citation_tot / publication_tot
        # o valor maximo do index H é o numero de trabalhos publicados
        hwos_max = len(ls_timewos)
        if hwos_max == 1:
            hwos = 1
        else:
            # ordem descrecente
            ls_timewos.sort(reverse=True)
            # hwos_freq frequencia do valor de hwos
            ncitat_hwos = 0
            hwos = hwos_max + 1
            while hwos > ncitat_hwos:
                hwos -= 1
                ncitat_hwos = len(
                    [xx for xx in ls_timewos if xx >= hwos])
    citation_avr = round(citation_avr, 2)
    df_hwebsci_allgroup = pd.DataFrame({'HWEBSCI': [hwos],
                                        'TOTAL_PUBLIC': [publication_tot],
                                        'TOTAL_CITATION': [citation_tot],
                                        'CITATION_AVR': [citation_avr]})
    df_hwebsci_allgroup.to_csv('./csv_producao_hindex/hindex_websci_allgroup_papers_summary.csv',
                               index=False)

    df_hwebsci_allgroup_papers = df_temp[
        df_temp['Total Citations'] >= hwos]
    df_hwebsci_allgroup_papers.reset_index(inplace=True, drop=True)
    df_hwebsci_allgroup_papers = df_hwebsci_allgroup_papers \
        .sort_values(['Total Citations'],
                     ascending=False)
    df_hwebsci_allgroup_papers.reset_index(drop=True, inplace=True)
    df_hwebsci_allgroup_papers = df_hwebsci_allgroup_papers.loc[
        :, ['Title', 'Source Title', 'Authors',
            'Total Citations']]
    df_hwebsci_allgroup_papers.reset_index(inplace=True, drop=True)
    df_hwebsci_allgroup_papers.to_csv(
        './csv_producao_hindex/hindex_websci_allgroup_papers_report.csv',
        index=False)

    return df_hwebsci_allgroup


def paper_citation_byyear(citation_year):
    """
    Return papers citations for a specific year.

    Parameters:
        year (int): Year of publication and citation
    Returns:
        a csv file into csv_producao_hindex
    """
    df = pd.read_csv('./csv_producao_hindex/hindex_websci_papers_uniq.csv',
                     header=0)
    dfyear = df.iloc[:, 0:21]
    dfyear[str(citation_year)] = df[str(citation_year)]
    dfyear = dfyear.reset_index(drop=True)
    dfyear = dfyear[dfyear['Publication Year'] == citation_year]
    dfyear = dfyear.reset_index(drop=True)
    dfyear = dfyear.sort_values([str(citation_year)], ascending=False) \
        .reset_index(drop=True)
    dfyear = dfyear.loc[:, ['Title', 'Source Title', 'Publication Year',
                            'Authors', str(citation_year)]]
    dfyear.to_csv(
        './csv_producao_hindex/citations_byyear_papers_report.csv',
        index=False)
