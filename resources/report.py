"""Generate a report file with tables and plots."""

from tabulate import tabulate
# from resources.support_functions import qualis_file
from resources.support_functions import pg_name
from resources.support_functions import yearlimit_forfilter
from resources.support_functions import report_resch_teach
from resources.support_functions import report_resch_books
from resources.support_functions import report_resch_chapters
from resources.support_functions import report_resch_ppe
from resources.support_functions import report_resch_papers
from resources.support_functions import report_resch_papers_group_all
from resources.support_functions import report_resch_papers_group_uniq
from resources.support_functions import report_resch_advi_done_pg
from resources.support_functions import report_resch_advi_runn_pg
from resources.support_functions import report_resch_advi_done_all
from resources.support_functions import report_resch_advi_runn_all
from resources.support_functions import report_resch_advi_done_each
from resources.support_functions import report_resch_advi_runn_each
from resources.support_functions import report_tbl_indexh
from resources.support_functions import report_tbl_indexh_uniq
from resources.support_functions import report_tbl_indexh_group_paper_summary
from resources.support_functions import report_tbl_indexh_group_paper_report
import pandas as pd
# import platform
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('fivethirtyeight')


def report_write(qf):
    """Generate a report file with tables and plots."""
    # qualqualis = qualis_file()
    qualqualis = qf
    lsyear_limits = yearlimit_forfilter()
    yyi, yyf = lsyear_limits[0], lsyear_limits[1]
    with open('./relatorio/report_setup.json', 'r') as jfile:
        rep_setup_file = json.load(jfile)
        jfile.close()

    # start write the report
    htmlfile = open('./relatorio/relatorio_producao.html', 'w')
    htmlfile.write('<!DOCTYPE html> \n ')
    htmlfile.write('<head> \n ')
    # verificando sistema
    # plat_sys = platform.system()
    # if plat_sys == 'Windows':
    # htmlfile.write(
    # '<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />  \n')
    # else:
    htmlfile.write(
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  \n')
    htmlfile.write(' <title>lucyLattes Relatorio</title> \n')
    htmlfile.write(
        '<link rel="stylesheet" href="./css/gitgub.css" type="text/css" /> \n </head> \n')
    htmlfile.write('</head> \n ')
    htmlfile.write('<body> \n')
    htmlfile.write('<h0 class="title">Relatório de Produção</h0> \n <br>\n')
    htmlfile.write('<small>Gerado por <i>lucyLattes.py</i>' + ' ' +
                   '<a href="https://github.com/rafatieppo/lucyLattes">https://github.com/rafatieppo/lucyLattes</a></small> \n <br> \n')
    htmlfile.write(
        '<a href="https://doi.org/10.5281/zenodo.2591748"> <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2591748.svg" alt="DOI"> </a>')

    # quick sumario
    htmlfile.write('<h1 class="title">Sumário</h1> \n')
    htmlfile.write('<a href="#team">Equipe</a> \n <br>')
    htmlfile.write('<a href="#projexte">Projetos de extensão</a> \n <br>')
    htmlfile.write('<a href="#projpesq">Projetos de pesquisa</a> \n <br>')
    htmlfile.write('<a href="#pubbookchap">Livros e capítulos</a> \n <br>')
    htmlfile.write('<a href="#pubperiod">Artigos em periódicos</a> \n <br>')
    htmlfile.write('<a href="#advperiod">Orientações</a> \n <br>')
    htmlfile.write(
        '<a href="#advrunnperiod">Orientações em andamento</a> \n <br>')
    htmlfile.write(
        '<a href="#prodporpesq">Produção individual</a> \n <br>')
    htmlfile.write(
        '<a href="#indh">Índice H - base webofknowledge</a> \n <br>')
    # htmlfile.write('<a href="#xxx">Indicadores CAPES</a> \n <br>')

    # equipe
    dffullname_all = pd.read_csv('./csv_producao/fullname_all.csv',
                                 header=0, dtype=str)
    dffullname_all = dffullname_all.sort_values(
        ['FULL_NAME']).reset_index(drop=True)
    for idx in range(len(dffullname_all)):
        htmlfile.write('<hr>')
        htmlfile.write('<b>Nome: </b>')
        htmlfile.write(dffullname_all['FULL_NAME'].iloc[idx])
        htmlfile.write('<br>')
        htmlfile.write('<b>Nascimento: </b>')
        htmlfile.write(dffullname_all['CITY'].iloc[idx])
        htmlfile.write(' - ')
        htmlfile.write(str(dffullname_all['STATE'].iloc[idx]))
        htmlfile.write('<br>')
        htmlfile.write('<b>Instituição: </b>')
        htmlfile.write(str(dffullname_all['ADDRESS_ENTERP'].iloc[idx]))
        htmlfile.write('<br>')
        htmlfile.write('<b>Resumo: </b>')
        htmlfile.write(str(dffullname_all['RESUME'].iloc[idx]))
        htmlfile.write('<p>')
        htmlfile.write('<b>Lattes: </b>')
        latteslink = 'http://lattes.cnpq.br/' + \
            str(dffullname_all['ID'].iloc[idx])
        htmlfile.write('<a href="' + latteslink + '">' + latteslink + '</a>')
        htmlfile.write('<br>')
        htmlfile.write('<b>Última atualização: </b>')
        lattesupda = str(dffullname_all['UPDATE'].iloc[idx])
        htmlfile.write(lattesupda + '<br>')
        htmlfile.write('<b>ORCID: </b>')
        htmlfile.write(str(dffullname_all['ORCID'].iloc[idx]))
        htmlfile.write('<br><br>')

    # Projetos de Extensao do Grupo
    htmlfile.write('<a name="projexte"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de extensão do grupo ' + str(yyi) + '-' +
                   str(yyf) + '</h1> \n')
    htmlfile.write('<small>Elimina duplicidade de projetos. </small> <br><br>')
    if rep_setup_file['ppe_uniq']['print'] == 'YES':
        dfppe_uniq_ext = pd.read_csv(
            './relatorio/csv_report/report_ppe_uniq.csv', header=0, dtype=str)
        dfppe_uniq_ext = dfppe_uniq_ext[dfppe_uniq_ext['NATURE'] == 'EXTENSAO']
        if len(dfppe_uniq_ext) > 1:
            dfppe_uniq_ext.reset_index(inplace=True, drop=True)
            dfppe_uniq_ext['YEAR'] = dfppe_uniq_ext['YEAR'].apply(
                lambda x: int(x))
            dfppe_uniq_ext['YEAR_FIN'] = dfppe_uniq_ext['YEAR_FIN'].apply(
                lambda x: int(x))
            dfppe_uniq_ext.sort_values(['YEAR'], inplace=True)
            dfppe_uniq_ext.reset_index(inplace=True, drop=True)
            htmlfile.write('<ol class="custom-counter">')
            for idx in range(len(dfppe_uniq_ext)):
                proj = dfppe_uniq_ext['TITLE'].iloc[idx]
                proj_yi = dfppe_uniq_ext['YEAR'].iloc[idx]
                proj_yf = dfppe_uniq_ext['YEAR_FIN'].iloc[idx]
                proj_au = dfppe_uniq_ext['MEMBERS'].iloc[idx]
                htmlfile.write('<li>' + '\n')
                htmlfile.write('<i>' + '\n')
                htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                               str(proj_yi) + '</u>.' +
                               ' fim: <u> ' + str(proj_yf)
                               + '.</u> ' + '<i>' + proj_au + '</i>.')
                htmlfile.write('\n </i>' + '\n')
                htmlfile.write('</li>' + '\n \n')
            htmlfile.write('</ol>')
        else:
            htmlfile.write('Não há projetos de extensão <br>\n')
    else:
        htmlfile.write('Não há projetos de extensão <br>\n')

    # research projects for the group
    htmlfile.write('<a name="projpesq"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de pesquisa do grupo ' + str(yyi) + '-' +
                   str(yyf) + '</h1> \n')
    htmlfile.write('<small>Elimina duplicidade de projetos. </small> <br><br>')
    if rep_setup_file['ppe_uniq']['print'] == 'YES':
        dfppe_uniq_resch = pd.read_csv(
            './relatorio/csv_report/report_ppe_uniq.csv', header=0, dtype=str)
        dfppe_uniq_resch = dfppe_uniq_resch[dfppe_uniq_resch['NATURE'] == 'PESQUISA']
        if len(dfppe_uniq_resch) >= 1:
            dfppe_uniq_resch.reset_index(inplace=True, drop=True)
            dfppe_uniq_resch['YEAR'] = dfppe_uniq_resch['YEAR'].apply(
                lambda x: int(x))
            dfppe_uniq_resch['YEAR_FIN'] = dfppe_uniq_resch['YEAR_FIN'].apply(
                lambda x: int(x))
            dfppe_uniq_resch.sort_values(['YEAR'], inplace=True)
            dfppe_uniq_resch.reset_index(inplace=True, drop=True)
            htmlfile.write('<ol class="custom-counter">')
            for idx in range(len(dfppe_uniq_resch)):
                proj = dfppe_uniq_resch['TITLE'].iloc[idx]
                proj_yi = dfppe_uniq_resch['YEAR'].iloc[idx]
                proj_yf = dfppe_uniq_resch['YEAR_FIN'].iloc[idx]
                proj_au = dfppe_uniq_resch['MEMBERS'].iloc[idx]
                htmlfile.write('<li>' + '\n')
                htmlfile.write('<i>' + '\n')
                htmlfile.write('<u>' + str(proj) + '</u>. início: <u>' +
                               str(proj_yi) + '</u>.' +
                               ' fim: <u> ' + str(proj_yf)
                               + '.</u> ' + '<i>' + proj_au + '</i>.')
                htmlfile.write('\n </i>' + '\n')
                htmlfile.write('</li>' + '\n \n')
            htmlfile.write('</ol>')
        else:
            htmlfile.write('Não há projetos de pesquisa <br>\n')
    else:
        htmlfile.write('Não há projetos de pesquisa <br>\n')

    # books and chapters
    # books report
    htmlfile.write('<a name="pubbookchap"></a>' + '\n \n')
    htmlfile.write('<h1>Livros e capítulos do grupo ' + str(yyi) + '-' +
                   str(yyf) + '</h1> \n')
    htmlfile.write(
        '<small>Elimina duplicidade de livros e capítulos. </small> <br><br>')
    htmlfile.write('<h2>Relação de livros do grupo ' + str(yyi) + '-' +
                   str(yyf) + '</h2> \n')
    if rep_setup_file['books_uniq']['print'] == 'YES':
        dfbooks_uniq = pd.read_csv(
            './relatorio/csv_report/report_books_uniq.csv', header=0, dtype=str)
        dfbooks_uniq['YEAR'] = dfbooks_uniq['YEAR'].apply(
            lambda x: int(x))
        dfbooks_uniq.sort_values(['YEAR'], inplace=True)
        dfbooks_uniq.reset_index(inplace=True, drop=True)
        htmlfile.write('<ol class="custom-counter">')
        for idx in range(len(dfbooks_uniq)):
            title = dfbooks_uniq['TITLE'].iloc[idx]
            proj_yi = dfbooks_uniq['YEAR'].iloc[idx]
            proj_au = dfbooks_uniq['AUTHOR'].iloc[idx]
            htmlfile.write('<li>' + '\n')
            htmlfile.write('<i>' + '\n')
            htmlfile.write('<u>' + str(title) + '</u>. ano: <u>' +
                           str(proj_yi) + '</u>.' +
                           '.</u> ' + '<i>' + proj_au + '</i>.')
            htmlfile.write('\n </i>' + '\n')
            htmlfile.write('</li>' + '\n \n')
        htmlfile.write('</ol>')

        # books by year plot and resume by fullname-year
        htmlfile.write('<h2>Produção de livros por ano ' + str(yyi) + '-' +
                       str(yyf) + '</h2> \n')
        book_gbyear = dfbooks_uniq.groupby(
            ['YEAR'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=book_gbyear['YEAR'], height=book_gbyear['TITLE'])
        plt.title('Livros  %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('Número de livros')
        plt.yticks(np.arange(0, book_gbyear['TITLE'].max() + 2, 1))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/books_byyear.png')
        # plt.show()
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/books_byyear.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write('<figcaption>Número de livros por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')
        book_gbfullnameyear = dfbooks_uniq.groupby(
            ['FULL_NAME', 'YEAR'])['TITLE'].size().unstack().reset_index(
                drop=False)
        book_gbfullnameyear.fillna(0, inplace=True)
        book_gbfullnameyear['TOTAL'] = book_gbfullnameyear.iloc[:, 1:].sum(
            axis=1)
        book_gbtitleyear_table = tabulate(book_gbfullnameyear, headers="keys",
                                          tablefmt='html')
        htmlfile.write(
            '<table_caption> TABELA: Relação de livros por autor \n' +
            '<small> (cada publicação e contabilizada apenas uma vez). \n <br>' +
            '</small> \n </table_caption>')
        htmlfile.write(book_gbtitleyear_table + '\n <br> \n <br> \n')
    else:
        htmlfile.write('Não há livros publicado para o grupo. <br>\n')

    # chapters report
    htmlfile.write('<h2>Relação de capítulos do grupo ' + str(yyi) + '-' +
                   str(yyf) + '</h2> \n')
    if rep_setup_file['chapters_uniq']['print'] == 'YES':
        dfchaps_uniq = pd.read_csv(
            './relatorio/csv_report/report_chapters_uniq.csv',
            header=0, dtype=str)
        dfchaps_uniq['YEAR'] = dfchaps_uniq['YEAR'].apply(
            lambda x: int(x))
        dfchaps_uniq.sort_values(['YEAR'], inplace=True)
        dfchaps_uniq.reset_index(inplace=True, drop=True)
        htmlfile.write('<ol class="custom-counter">')
        for idx in range(len(dfchaps_uniq)):
            title = dfchaps_uniq['TITLE'].iloc[idx]
            proj_yi = dfchaps_uniq['YEAR'].iloc[idx]
            proj_au = dfchaps_uniq['AUTHOR'].iloc[idx]
            htmlfile.write('<li>' + '\n')
            htmlfile.write('<i>' + '\n')
            htmlfile.write('<u>' + str(title) + '</u>. ano: <u>' +
                           str(proj_yi) + '</u>.' +
                           '.</u> ' + '<i>' + proj_au + '</i>.')
            htmlfile.write('\n </i>' + '\n')
            htmlfile.write('</li>' + '\n \n')
        htmlfile.write('</ol>')

        # chapters by year plot and resume by fullname-year
        htmlfile.write('<h2>Produção de capítulos por ano ' + str(yyi) + '-' +
                       str(yyf) + '</h2> \n')
        chapp = dfchaps_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=chapp['YEAR'], height=chapp['TITLE'])
        plt.title('Capítulos  %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('Número de livros')
        plt.yticks(np.arange(0, chapp['TITLE'].max() + 2, 1))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/chapters_byyear.png')
        # plt.show()
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/chapters_byyear.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Número de capítulos por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')
        chap_gbfullnameyear = dfchaps_uniq.groupby(
            ['FULL_NAME', 'YEAR'])['TITLE'].size().unstack().reset_index(
                drop=False)
        chap_gbfullnameyear.fillna(0, inplace=True)
        chap_gbfullnameyear['TOTAL'] = chap_gbfullnameyear.iloc[:, 1:].sum(
            axis=1)
        chap_gbfullnameyear_table = tabulate(chap_gbfullnameyear,
                                             headers="keys", tablefmt='html')
        htmlfile.write(
            '<table_caption> TABELA: Relação de capítulos por autor \n' +
            '<small> (cada publicação é contabilizada apenas uma vez). \n <br>' +
            '</small> \n </table_caption>')
        htmlfile.write(chap_gbfullnameyear_table + '\n <br> \n <br> \n')
    else:
        htmlfile.write('Não há capítulos publicados para o grupo. <br>\n')

    # Publicacao em periodicos
    htmlfile.write('<a name="pubperiod"></a>' + '\n \n')
    htmlfile.write('<h1>Publicação em periódicos</h1> \n')
    htmlfile.write(
        '<small>Elimina duplicidade de artigos. </small> <br><br>')
    # papers report
    htmlfile.write('<h2>Relação de artigos em periódicos do grupo ' +
                   str(yyi) + '-' + str(yyf) + '</h2> \n')
    if rep_setup_file['papers_uniq']['print'] == 'YES':
        dfpapers_uniq = pd.read_csv(
            './relatorio/csv_report/report_papers_uniq.csv',
            header=0, dtype=str)
        dfpapers_uniq['YEAR'] = dfpapers_uniq['YEAR'].apply(
            lambda x: int(x))
        dfpapers_uniq.sort_values(['YEAR'], inplace=True)
        dfpapers_uniq.reset_index(inplace=True, drop=True)
        htmlfile.write('<ol class="custom-counter">')
        for idx in range(len(dfpapers_uniq)):
            title = dfpapers_uniq['TITLE'].iloc[idx]
            proj_yi = dfpapers_uniq['YEAR'].iloc[idx]
            proj_au = dfpapers_uniq['AUTHOR'].iloc[idx]
            proj_qualis = dfpapers_uniq['QUALIS'].iloc[idx]
            proj_jcr = dfpapers_uniq['JCR'].iloc[idx]
            htmlfile.write('<li>' + '\n')
            htmlfile.write('<i>' + '\n')
            htmlfile.write('<u>' + str(title) + '</u>. ano: <u>' +
                           str(proj_yi) + '</u>.' +
                           '.</u> ' + '<i>' + proj_au + '</i>.' +
                           ' qualis: <b>' + str(proj_qualis) + '</b>' +
                           ' jcr: <b>' + str(proj_jcr) + '</b>')
            htmlfile.write('\n </i>' + '\n')
            htmlfile.write('</li>' + '\n \n')
        htmlfile.write('</ol>')

        # papers by year plot and resume by fullname-year
        htmlfile.write('<h2>Produção de  artigos por ano ' + str(yyi) + '-' +
                       str(yyf) + '</h2> \n')
        paperp = dfpapers_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=paperp['YEAR'], height=paperp['TITLE'])
        plt.title('Artigos  %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('Número de artigos')
        plt.yticks(np.arange(0, paperp['TITLE'].max() + 2, 2))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/papers_byyear.png')
        # plt.show()
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/papers_byyear.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Número de artigos por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')

        # papers by year / fullname
        papr_gbfullnameyear = dfpapers_uniq.groupby(
            ['FULL_NAME', 'YEAR'])['TITLE'].size().unstack().reset_index(
                drop=False)
        papr_gbfullnameyear.fillna(0, inplace=True)
        papr_gbfullnameyear['TOTAL'] = papr_gbfullnameyear.iloc[:, 1:].sum(
            axis=1)
        lstot = papr_gbfullnameyear.iloc[:, 1:].sum(axis=0).to_list()
        lstot.insert(0, 'Total')
        papr_gbfullnameyear = pd.concat(
            [papr_gbfullnameyear,
             pd.DataFrame([lstot],
                          columns=list(papr_gbfullnameyear.columns))],
            axis=0).reset_index(drop=True)
        papr_gbfullnameyear_table = tabulate(papr_gbfullnameyear,
                                             headers="keys", tablefmt='html')
        htmlfile.write(
            '<table_caption> TABELA: Relação de artigos por autor/ano \n' +
            '<small> (cada publicação é contabilizada apenas uma vez). \n <br>' +
            '</small> \n </table_caption>')
        htmlfile.write(papr_gbfullnameyear_table + '\n <br> \n <br> \n')

        # papers by qualis / fullname plot and summary
        htmlfile.write('<h2>Produção de artigos por qualis ' + str(yyi) + '-' +
                       str(yyf) + '</h2> \n')
        htmlfile.write('<p>Nesta secção é apresentada a relação da produção de ' +
                       'artigos classificada pelo qualis. ' +
                       'Sendo que na Figura e na primeira Tabela, ' +
                       'cada publicação é contabilizada para apenas um' +
                       'autor. Na segunda Tabela a mesma publicação é ' +
                       'contabilizada para mais de um autor.</p>')

        paperq = dfpapers_uniq.groupby(
            ['QUALIS'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=paperq['QUALIS'], height=paperq['TITLE'])
        plt.title('Artigos  %i - %i' % (yyi, yyf))
        # plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Qualis')
        plt.ylabel('Número de artigos')
        plt.yticks(np.arange(0, paperq['TITLE'].max() + 2, 3))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/papers_byqualis.png')
        # plt.show()
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/papers_byqualis.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Número de artigos por classificação Qualis.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')

        # table for paper author/qualis with out duplicate
        papr_gbfullnamequal_table_uniq = report_resch_papers_group_uniq(
            rep_setup_file)
        htmlfile.write(
            '<table_caption> TABELA: Relação de artigos por autor/qualis' +
            '<small> (cada publicação é contabilizada para apenas um autor). \n <br>' +
            '</small> \n </table_caption>')
        htmlfile.write(papr_gbfullnamequal_table_uniq + '\n <br> \n <br> \n')

        # table for paper author/qualis with duplicate
        papr_gbfullnamequal_table = report_resch_papers_group_all(
            rep_setup_file)
        htmlfile.write(
            '<table_caption> TABELA: Relação de artigos por autor/qualis' +
            '<small> (publicação pode ser contabilizada para mais de um autor). \n <br>' +
            '</small> \n </table_caption>')
        htmlfile.write(papr_gbfullnamequal_table + '\n <br> \n <br> \n')

        # researchers interactions graph in papers
        htmlfile.write('<h2>Interação entre pesquisadores ' + str(yyi) + '-' +
                       str(yyf) + '</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/grapho_paper.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Grafo de colaboração entre pesquisadores apenas em ' +
            'artigos</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <br> \n \n')
        # Lista de profissionais sem interacao em periodicos
        if rep_setup_file['grapho_papernoint']['print'] == 'YES':
            dfpapers_withnointer = pd.read_csv(
                './relatorio/csv_report/report_papers_withno_interact.csv',
                header=0, dtype=str)
            lspapers_withnointer = dfpapers_withnointer['FULL_NAME'].to_list()
            htmlfile.write(
                '<b><i>Não foi possível localizar interações em periódicos' +
                ' para os seguintes pesquisadores: </i></b><br> \n')
            htmlfile.write('<ul>')
            for idy in range(len(lspapers_withnointer)):
                name = lspapers_withnointer[idy]
                htmlfile.write('<b style="color:gray;"> <li>' +
                               name + '</li> </b> \n')
            htmlfile.write('\n </ul> \n')
            htmlfile.write('\n <hr> \n \n')
    else:
        htmlfile.write('Não há artigo publicado para o grupo. <br>\n')

    # orientacoes
    htmlfile.write('<a name="advperiod"></a>' + '\n \n')
    htmlfile.write('<h1>Orientações concluídas ' + str(yyi) + '-' +
                   str(yyf) + '</h1> \n')
    htmlfile.write('<p>Nesta secção é apresentada a relação das orientações ' +
                   'concluidas dos pesquisadores. Na primeira Tabela consta um resumo ' +
                   'do número de orientações de Mestrado e Doutorado ' +
                   'no PG concluídas no período definido. Na segunda Tabela consta ' +
                   'a relação de todas as orientações concluídas do pesquisador. ' +
                   'Para consultar o nome do orientado e demais detalhes, ' +
                   'consulte a produção individual do pesquisador.</p><br>')

    pgname = pg_name()
    adv_table_donepg = report_resch_advi_done_pg(rep_setup_file, pgname)
    htmlfile.write(
        '\n <table_caption> TABELA: Relação de orientações de Mestrado e ' +
        'Doutorado concluídas em ' +
        str(yyi) + '-' + str(yyf) + ' no PG ' + str(pgname) +
        ' (<small> possibilidade de contabilizar co-orientação</small>) ' +
        '\n </table_caption>')
    htmlfile.write(adv_table_donepg + '\n <br> \n <br> \n')

    adv_table_done = report_resch_advi_done_all(rep_setup_file)
    htmlfile.write(
        '\n <table_caption> TABELA: Relação de todas as orientações ' +
        'concluídas em ' + str(yyi) + '-' + str(yyf) +
        ' em diversos cursos (<small> ' +
        'possibilidade de contabilizar co-orientação</small>) ' +
        '\n</table_caption>')
    htmlfile.write('<small>\n ' + adv_table_done + '\n </small>\n')
    htmlfile.write('<small>' +
                   'MEST: dissertação; POS-DOC: pós doutoramento; ' +
                   'TCC: trabalho conclusão de curso; ' +
                   'IC: inciação científica; DOUT: tese; ' +
                   'MONO-ESP: monografia-especialização; ' +
                   'OUTRA: outra orientação \n</small>')

    # orientacoes em andamento
    htmlfile.write('<a name="advrunnperiod"></a>' + '\n \n')
    htmlfile.write('<h1>Orientações em andamento </h1>\n')
    # + str(yyi) + '-' + str(yyf) + '</h1> \n')
    htmlfile.write('<p>Nesta secção é apresentada a relação das orientações ' +
                   'em andamento dos pesquisadores. Na primeira Tabela  ' +
                   'consta um resumo do número de orientações de Mestrado e ' +
                   'Doutorado em andamento no PG. Na segunda Tabela consta a ' +
                   'relação de todas as orientações em andamento do pesquisador. ' +
                   'Para consultar o nome do orientado e demais detalhes, ' +
                   'consulte a produção individual do pesquisador.</p><br>')

    pgname = pg_name()
    adv_table_runnpg = report_resch_advi_runn_pg(rep_setup_file, pgname)
    htmlfile.write(
        '\n <table_caption> TABELA: Relação de orientações de Mestrado e ' +
        'Doutorado em andamento ' +  # str(yyi) + '-' + str(yyf) +
        'no PG ' + str(pgname) +
        '(<small> possibilidade de contabilizar co-orientação</small>) ' +
        '\n </table_caption>')
    htmlfile.write(adv_table_runnpg + '\n <br> \n <br> \n')

    adv_table_runn = report_resch_advi_runn_all(rep_setup_file)
    htmlfile.write(
        '\n <table_caption> TABELA: Relação de todas as orientações em ' +
        'andamento ' +  # + str(yyi) + '-' + str(yyf) +
        ' em diversos cursos (<small> ' +
        'possibilidade de contabilizar co-orientação</small>) ' +
        '\n</table_caption>')
    htmlfile.write('<small>\n ' + adv_table_runn + '\n </small>\n')
    htmlfile.write('<small>' +
                   'MEST: dissertação; POS-DOC: pós doutoramento; ' +
                   'TCC: trabalho conclusão de curso; ' +
                   'IC: inciação científica; DOUT: tese; ' +
                   'MONO-ESP: monografia-especialização; ' +
                   'OUTRA: outra orientação \n</small>')

    # ------------------------------------------------------------
    # producao individual dos pesquisadores
    htmlfile.write('<a name="prodporpesq"></a>' + '\n \n')
    htmlfile.write('<h1>Produção individual ' + str(yyi) + '-' +
                   str(yyf) + '</h1> \n')
    htmlfile.write('<p>Nesta secção é apresentada a relação da produção ' +
                   'individual dos pesquisadores. As produções ' +
                   'summarizadas são: Aulas ministradas, projetos de  ' +
                   'extensão, projetos de pesquisa, livros, capítulos e ' +
                   'artigos (contabilizados para mais de um autor.</p><br>')

    # finding all ids
    dfallids = pd.read_csv('./csv_producao/fullname_all.csv',
                           header=0, dtype=str)
    dfallids = dfallids.sort_values(['FULL_NAME']).reset_index(drop=True)
    lsallids = dfallids['ID'].to_list()
    for idx in range(len(lsallids)):
        # htmlfile.write('\n <div id="divActivites" name="divActivites" ' +
        #                'style="border:1px dotted grey;"> ')
        htmlfile.write('\n <div class="box"> \n')
        htmlfile.write('<h2>' + dfallids['FULL_NAME'].iloc[idx] +
                       '</h2>')
        latteslink = 'http://lattes.cnpq.br/' + str(dfallids['ID'].iloc[idx])
        htmlfile.write('- ' + '<a href="' + latteslink + '">' +
                       latteslink + '</a> ')
        lattesupda = str(dfallids['UPDATE'].iloc[idx])
        htmlfile.write('(atualizado em: ' +
                       lattesupda + ') <br> <br>')

        # teaching
        tbl_teach = report_resch_teach(lsallids[idx], rep_setup_file)
        htmlfile.write('<table_caption>TABELA: Disciplinas ministradas ' +
                       str(yyi) + '-' + str(yyf) + '\n</table_caption>\n<br>')
        htmlfile.write('<small>')
        htmlfile.write(tbl_teach + '\n')
        htmlfile.write('YI = ano inicial; YF = ano final; ' +
                       'MI = mês inicial; MF = mês final;.')
        htmlfile.write('</small><br><br>\n')

        # projects
        htmlfile.write('<table_caption>TABELA: Projetos de pesquisa e extensão ' +
                       str(yyi) + '-' + str(yyf) + '</table_caption><br>\n')
        tbl_ppes = report_resch_ppe(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_ppes + '\n')
        htmlfile.write('<small><i>nota: quando aparecem, a coluna <b>NAO</b>' +
                       ' indica se o pesquisador Não é coordenador, e ' +
                       'a coluna <b>SIM</b> o oposto, sendo 0 (zero) como ' +
                       'nulo e 1 (um) para nao nulo.</i></small> <br><br>\n')

        # advising
        htmlfile.write('<table_caption>TABELA: Orientações concluídas em ' +
                       str(yyi) + '-' + str(yyf) + '</table_caption><br>\n')
        tbl_adv = report_resch_advi_done_each(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_adv + '\n')
        htmlfile.write('<small>' +
                       'MEST: dissertação; POS-DOC: pós doutoramento; ' +
                       'TCC: trabalho conclusão de curso; ' +
                       'IC: inciação científica; DOUT: tese; ' +
                       'MONO-ESP: monografia-especialização; ' +
                       'OUTRA: outra orientação \n</small><br><br><br>')

        # advising running
        htmlfile.write('<table_caption>TABELA: Orientações em andamento ' +
                       # str(yyi) + '-' + str(yyf) +
                       '</table_caption><br>\n')
        tbl_adv = report_resch_advi_runn_each(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_adv + '\n')
        htmlfile.write('<small>' +
                       'MEST: dissertação; POS-DOC: pós doutoramento; ' +
                       'TCC: trabalho conclusão de curso; ' +
                       'IC: inciação científica; DOUT: tese; ' +
                       'MONO-ESP: monografia-especialização; ' +
                       'OUTRA: outra orientação \n</small><br><br><br>')

        # books
        htmlfile.write('<table_caption>TABELA: Livros publicados ' +
                       str(yyi) + '-' + str(yyf) + '</table_caption><br>\n')
        tbl_books = report_resch_books(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_books + '\n <br><br> \n')

        # chapters
        htmlfile.write('<table_caption>TABELA: Capítulos publicados ' +
                       str(yyi) + '-' + str(yyf) + '</table_caption><br>\n')
        tbl_chapters = report_resch_chapters(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_chapters + '\n <br> <br> <br> \n')

        # papers
        htmlfile.write('<table_caption>TABELA: Artigos publicados ' +
                       str(yyi) + '-' + str(yyf) + '</table_caption><br>\n')
        tbl_papers = report_resch_papers(lsallids[idx], rep_setup_file)
        htmlfile.write(tbl_papers + '\n <br> \n <br> \n')
        # rule
        htmlfile.write('<hr>')
        htmlfile.write('\n </div> \n')

    # INDICE H WEBOFSCI ----------------------------------------------
    htmlfile.write('<a name="indh"></a>' + '\n \n')
    htmlfile.write('<h1 class="title">Índice H - base webofknowledge</h1> \n')
    htmlfile.write('<p> O índice H é um valor baseado sobre a relação da' +
                   'produção ordenada em função do número de citações de' +
                   'cada artigo em ordem descrescente para cada pesquisador.' +
                   'O índice H siginifica que há h artigos e que cada um  ' +
                   'deles foi citado pelo menos h vezes. Ou seja, o índice  ' +
                   'H nunca será maior que o número de artigos publicados ' +
                   'pelo pesquisador. Dessa forma, o índice H associa a ' +
                   'qualidade e quantidade dos produtos do pesquisador.\n</p>')
    htmlfile.write(
        '<p>A base utilizada para estes estudo foi a Web of Science ' +
        '(apps-webofknowledge)</p>')

    if rep_setup_file['hwebofsci']['print'] == 'YES':
        htmlfile.write(
            '<h4><u>Índice H considerando duplicidade de artigos</h4> <br>\n')
        # str(int(yyi)) + '-' + str(int(yyf)) + '</u></h4> <br>\n')
        tabl = report_tbl_indexh(rep_setup_file)
        htmlfile.write(tabl)
        htmlfile.write(
            '<small>A citação média é o total de citações dividido ' +
            'pelo  número total de artigos para cada pesquisador. ' +
            '</small> <br>\n')
        htmlfile.write('<figure> \n')
        htmlfile.write(
            '<img src="./figures/hindex_websci_papers_tbl.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Índice H webofknowledge dos pesquisadores do PPG.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')

    if rep_setup_file['hwebofsci_uniq']['print'] == 'YES':
        htmlfile.write(
            '<h4><u>Índice H excluindo duplicidade de artigos</u></h4><br>\n')
        # str(int(yyi)) + '-' + str(int(yyf)) + '</u></h4> <br>\n')
        tabl = report_tbl_indexh_uniq(rep_setup_file)
        htmlfile.write(tabl)
        htmlfile.write(
            '<small>A citação média é o total de citações dividido pelo ' +
            'número total de artigos para cada pesquisador. <br></small>\n')
        htmlfile.write('<figure> \n')
        htmlfile.write(
            '<img src="./figures/hindex_websci_papers_tbl_uniq.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Índice H webofknowledge dos pesquisadores do PPG ' +
            'excluindo duplicidade de artigos.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')

        # indexH para all GRUPO com exclusao de duplicidade
        htmlfile.write(
            '<h4><u>Índice H PARA O GRUPO excluindo duplicidade de artigos' +
            '</u></h4><br>\n')
        # str(int(yyi)) + '-' + str(int(yyf)) + '</u></h4> <br>\n')
        tabl = report_tbl_indexh_group_paper_summary()
        htmlfile.write(tabl)
        htmlfile.write(
            '<small>A citação média é o total de citações dividido pelo  ' +
            'número total de artigos para cada pesquisador.<br><br></small>\n')

        # relacao de artigos para index H do grupo
        htmlfile.write(
            '<h4><u>Relação de artigos em periódicos para Índice H do GRUPO' +
            '</u></h4> <br>\n ')
        # str(int(yyi)) + '-' + str(int(yyf)) + '</u></h4> <br>\n')
        tabl = report_tbl_indexh_group_paper_report()
        htmlfile.write(tabl)
        htmlfile.write('\n <hr> \n \n')

    # warnings
    htmlfile.write('<b>AVISOS</b>:\n ')
    htmlfile.write(
        '<li>Arquivo para classificacao qualis utilizado: <code>'
        + qualqualis + '</code >')
    htmlfile.write(
        '<li>Os resultados estão sujeitos a falhas devido a inconsistencias ' +
        'no preenchimento dos CVs Lattes</li>\n')
    htmlfile.write(
        '<li>O arquivo relatorio_producao.html foi gerado na pasta relatorio' +
        '</li>\n')
    htmlfile.write(
        '<li>Caso precise citar é possível usar o ' +
        'DOI: 10.5281/zenodo.2591748</li>\n')
    htmlfile.write('<br> <br> <br>')
    htmlfile.write('<footer> \n')
    htmlfile.write(
        'Relatório gerado por lucyLattes v2. Os resultados estão sujeitos a ' +
        'falhas devido a inconsistências no preenchimento dos CVs Lattes. ')
    htmlfile.write('Usualemte há falhas para excluir os artigos publicados ' +
                   'por mais de um pesquisador do grupo, pois os processos ' +
                   'de exclusão são baseados nos títulos e nem sempre os ' +
                   'mesmos são digitados corretamente no cv Lattes.')
    htmlfile.write('\n <br>')
    htmlfile.write('</footer> \n')
    htmlfile.close()
    print('------------------------------------------------------------')
    print('AVISOS')
    print('------------------------------------------------------------')
    print('- Arquivo para classificacao qualis utilizado: ' + qualqualis + '.')
    print('- Os resultados estão sujeitos a falhas devido a inconsistencias ' +
          'no preenchimento dos CVs Lattes.')
    print('- O arquivo extrato_periodico_autorqualis.csv foi gerado na ' +
          'pasta relatorio.')
    print('- O arquivo relatorio_producao.html foi gerado na pasta relatorio.')
    print('------------------------------------------------------------')
