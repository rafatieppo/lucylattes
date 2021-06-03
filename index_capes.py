# ------------------------------------------------------------
# packages
# ------------------------------------------------------------
# ------------------------------------------------------------
import numpy as np
import pandas as pd
import os
import glob
import re
from readidlist import readIdList
from extrafuns import *
# ------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------


def capes_indori():
    # nome ppg
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    name_ppg = config_file.readlines()[8].split(':')[1]
    name_ppg = name_ppg.rstrip('\n')
    name_ppg = name_ppg.strip(' ')
    name_ppg = fun_uppercase(name_ppg)
    config_file.close()
    # lendo pesquisadores
    df_idlist = readIdList()
    num_dp = len(df_idlist)
    # lendo orientacoes_all
    df = pd.read_csv('./csv_producao/orientacoes_all.csv',
                     header=0, sep=',')
    df = df.query('NATURE == "Dissertação de mestrado" \
                   or NATURE == "Tese de doutorado"')
    df = df.query('TYPE != "CO_ORIENTADOR"').reset_index(drop=True)
    df['COURSE'] = df['COURSE'].apply(fun_uppercase)
    df = df.query('COURSE == @name_ppg')
    # identificando os ppg dos pesquisadores
    ls_ppgs = df['COURSE'].unique()
    ls_ppgs.sort()
    ls_ppgs = ", ".join(ls_ppgs)
    # print('------------------------------------------------------------')
    # print("PPGs listados nos curriculos dos pesquisadores: ", ls_ppgs)
    # print('------------------------------------------------------------')
    # print("PPG a ser avaliado: ", name_ppg)
    # print('------------------------------------------------------------')
    # definindo os quadrienios
    year_fquadrien = 2013
    ls_quadri = [year_fquadrien]
    for i in range(5):
        year_fquadrien = year_fquadrien + 4
        ls_quadri.append(year_fquadrien)
        # print(ls_quadri)
    # calculo para cada trienio
    ls_yini_quad = []
    ls_yfin_quad = []
    ls_indori = []
    for i in range(len(ls_quadri)):
        yini = ls_quadri[i]
        yfin = ls_quadri[i] + 3
        # print('Quadrienio', yini, ' - ', yfin)
        df_qtdby_yradv = df.groupby(['YEAR', 'NATURE'])[
            'STUDENT'].count().reset_index()
        # print(df_qtdby_yradv)
        df_qtdby_yradv.query('YEAR >= @yini and YEAR <= @yfin', inplace=True)
        if len(df_qtdby_yradv) < 1:
            pass
        else:
            df_qtdby_yradv['PESO_DEF'] = df_qtdby_yradv['NATURE'].apply(
                fun_peso_defesa)
            df_qtdby_yradv['PROD_STUPESO'] = (df_qtdby_yradv['STUDENT'] *
                                              df_qtdby_yradv['PESO_DEF'])
            df_qtdby_yradv = df_qtdby_yradv.groupby(
                ['YEAR'])['PROD_STUPESO'].sum() / num_dp
            df_qtdby_yradv = df_qtdby_yradv.reset_index()
            df_qtdby_yradv.columns = ['YEAR', 'INDORI']
            indori_quad = df_qtdby_yradv['INDORI'].mean()
            ls_yini_quad.append(yini)
            ls_yfin_quad.append(yfin)
            ls_indori.append(round(indori_quad, 3))
            # print(df_qtdby_yradv)
            # print(indori_quad)
    df_indori = pd.DataFrame({'QUADRIENIO_INI': ls_yini_quad,
                              'QUADRIENIO_FIM': ls_yfin_quad,
                              'INDORI': ls_indori})
    df_indori['INDORI_CLASSIFICACAO'] = df_indori['INDORI'].apply(
        fun_indori_classif)
    pathfilename = str('./csv_producao/' + 'capesindex_indori'  '.csv')
    df_indori.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_indori), ' quadrienios')
    # print(df_indori)


def capes_indprodart():
    # lendo pesquisadores
    df_idlist = readIdList()
    num_dp = len(df_idlist)
    # lendo periodicos_uniq
    df = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                     header=0, sep=',')
    num_period_tot = len(df['QUALIS'])
    df.query('QUALIS != "XX"', inplace=True)
    df.query('QUALIS != "C "', inplace=True)
    df['YEAR'] = df['YEAR'].apply(iint)
    num_period_semqualis = num_period_tot - len(df['QUALIS'])
    print('Numero de periodicos sem QUALIS = ', num_period_semqualis)
    # definindo os quadrienios
    year_fquadrien = 2013
    ls_quadri = [year_fquadrien]
    for i in range(5):
        year_fquadrien = year_fquadrien + 4
        ls_quadri.append(year_fquadrien)
        # print(ls_quadri)
    # calculo para cada trienio
    ls_yini_quad = []
    ls_yfin_quad = []
    ls_indprodart = []
    for i in range(len(ls_quadri)):
        yini = ls_quadri[i]
        yfin = ls_quadri[i] + 3
        df_qtdby_qualis = df.groupby(['YEAR', 'QUALIS'])[
            'TITLE'].count().reset_index()
        df_qtdby_qualis.columns = ['YEAR', 'QUALIS', 'AMOUNT']
        # print(df_qtdby_qualis)
        df_qtdby_qualis.query('YEAR >= @yini and YEAR <= @yfin', inplace=True)
        if len(df_qtdby_qualis) < 1:
            pass
        else:
            # print('Quadrienio', yini, ' - ', yfin)
            df_qtdby_qualis['PESO'] = df_qtdby_qualis['QUALIS'].apply(
                fun_indprodart_classif)
            df_qtdby_qualis['PROD_AMOUPESO'] = df_qtdby_qualis['AMOUNT'] * \
                df_qtdby_qualis['PESO']
            # verificando representatividade B4 e B5 deve ser <= 0.2 por ano
            # print(df_qtdby_qualis)
            df_grade_tot_year = df_qtdby_qualis.groupby(
                ['YEAR'])['PROD_AMOUPESO'].sum().reset_index()
            df_qtdby_qualis_b4b5 = df_qtdby_qualis.query(
                'QUALIS == "B4" or QUALIS == "B5"')
            # print(df_grade_tot_year)
            # print(df_qtdby_qualis_b4b5)
            ls_years_b4b5_uniq = df_qtdby_qualis_b4b5['YEAR'].unique()
            for ia in range(len(ls_years_b4b5_uniq)):
                year_b4b5 = ls_years_b4b5_uniq[ia]
                df_yearb4b5 = df_qtdby_qualis_b4b5.query('YEAR == @year_b4b5')
                grade_tot_year_b4b5 = df_yearb4b5['PROD_AMOUPESO'].sum()
                df_temp = df_grade_tot_year.query('YEAR == @year_b4b5')
                grade_tot_year = df_temp['PROD_AMOUPESO'].sum()
                # print('Ano ', str(year_b4b5), 'B4 e B5 representam: ',
                #       str(round(grade_tot_year_b4b5 / grade_tot_year, 2)))
                if grade_tot_year_b4b5 / grade_tot_year > 0.2:
                    print('Para o ano ', str(year_b4b5),
                          'artigos B4 B5 glosados, maior que 0.2')
                    df_qtdby_qualis.query(
                        'YEAR != @year_b4b5 and QUALIS != "B4"', inplace=True)
                    df_qtdby_qualis.query(
                        'YEAR != @year_b4b5 and QUALIS != "B5"', inplace=True)
            df_qtdby_qualis = df_qtdby_qualis.groupby(
                ['YEAR'])['PROD_AMOUPESO'].sum() / num_dp
            df_qtdby_qualis = df_qtdby_qualis.reset_index()
            df_qtdby_qualis.columns = ['YEAR', 'INDPRODART']
            indprodart = df_qtdby_qualis['INDPRODART'].mean()
            ls_indprodart.append(indprodart)
            ls_yini_quad.append(yini)
            ls_yfin_quad.append(yfin)
    df_indprodart = pd.DataFrame({'QUADRIENIO_INI': ls_yini_quad,
                                  'QUADRIENIO_FIM': ls_yfin_quad,
                                  'INDPRODART': ls_indprodart})
    pathfilename = str('./csv_producao/' + 'capesindex_indprodart'  '.csv')
    df_indprodart.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_indprodart), ' quadrienios')
    # print(df_qtdby_qualis_b4b5)
    # print(df_qtdby_qualis)
    # print(df_indprodart)


def capes_indautdis():
    # nome ppg
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    name_ppg = config_file.readlines()[8].split(':')[1]
    name_ppg = name_ppg.rstrip('\n')
    name_ppg = name_ppg.strip(' ')
    name_ppg = fun_uppercase(name_ppg)
    config_file.close()
    # lendo pesquisadores
    df_idlist = readIdList()
    num_dp = len(df_idlist)
    # lendo orientacoes_all
    df = pd.read_csv('./csv_producao/orientacoes_all.csv',
                     header=0, sep=',')
    df = df.query('NATURE == "Dissertação de mestrado" \
                   or NATURE == "Tese de doutorado"')
    df = df.query('TYPE != "CO_ORIENTADOR"').reset_index(drop=True)
    df['COURSE'] = df['COURSE'].apply(fun_uppercase)
    df['STUDENT'] = df['STUDENT'].apply(fun_uppercase)
    df['FULL_NAME'] = df['FULL_NAME'].apply(fun_uppercase)
    df = df.query('COURSE == @name_ppg')
    # identificando os ppg dos pesquisadores
    ls_ppgs = df['COURSE'].unique()
    ls_ppgs.sort()
    ls_ppgs = ", ".join(ls_ppgs)
    # print('------------------------------------------------------------')
    # print("PPGs listados nos curriculos dos pesquisadores: ", ls_ppgs)
    # print('------------------------------------------------------------')
    # print("PPG a ser avaliado: ", name_ppg)
    # print('------------------------------------------------------------')
    # definindo os quadrienios
    year_fquadrien = 2013
    ls_quadri = [year_fquadrien]
    df_indautdisc_all = pd.DataFrame(
        columns=['QUADRIENIO', 'STUDENT', 'DOCENTE', 'TYPE', 'AMOUNT'])
    for i in range(5):
        year_fquadrien = year_fquadrien + 4
        ls_quadri.append(year_fquadrien)
        # print(ls_quadri)
    # calculo para cada trienio
    for i in range(len(ls_quadri)):
        ls_yini_quad = []
        ls_yfin_quad = []
        ls_disc = []
        ls_doce = []
        ls_disc_type_prod = []
        ls_disc_amount_prod_period = []
        yini = ls_quadri[i]  # egressos ate 5 anos
        yfin = ls_quadri[i] + 3
        # print('Quadrienio', yini, ' - ', yfin)
        df_disc_quadri = df.query('YEAR >= @yini+3-4 and YEAR <= @yfin+3')
        df_disc_quadri
        if len(df_disc_quadri) < 1:
            print("sem orientacoes para o periodo")
            pass
        else:
            ls_disc_period = list(df_disc_quadri['STUDENT'])
            ls_doce_period = list(df_disc_quadri['FULL_NAME'])
            df_period_all = pd.read_csv('./csv_producao/periodicos_all.csv',
                                        header=0, sep=',')
            df_period_all['AUTHOR'] = df_period_all['AUTHOR'].apply(
                fun_uppercase)
            for ia in range(len(ls_disc_period)):
                period_count = 0
                for ib in range(len(df_period_all)):
                    # print(ia.upper(), '---', df_period_all.iloc[ib, 7])
                    zdis = ls_disc_period[ia].split(' ')[-1]
                    zdoc = ls_doce_period[ia].split(' ')[-1]
                    zaut = df_period_all['AUTHOR'].iloc[ib]
                    if zdis in zaut and zdoc in zaut:
                        period_count += 1
                disc_type_prod = 'periodico'
                quadr = str(str(yini) + '-' + str(yfin))
                ls_disc.append(ls_disc_period[ia])
                ls_doce.append(ls_doce_period[ia])
                ls_disc_type_prod.append(disc_type_prod)
                ls_disc_amount_prod_period.append(period_count)
                ls_quad = np.repeat(quadr, len(ls_disc))
                df_indautdisc = pd.DataFrame(list(zip(ls_quad,
                                                      ls_disc,
                                                      ls_doce,
                                                      ls_disc_type_prod,
                                                      ls_disc_amount_prod_period)),
                                             columns=['QUADRIENIO', 'STUDENT', 'DOCENTE', 'TYPE', 'AMOUNT'])
            df_indautdisc_all = pd.concat([df_indautdisc_all,
                                           df_indautdisc])
    ls_indautdisc_quad = []
    ls_indautdisc = []
    ls_indis = []
    quad_indautdisc = df_indautdisc_all['QUADRIENIO'].unique()
    for i in range(len(quad_indautdisc)):
        q = quad_indautdisc[i]
        df_d = df_indautdisc_all.query('QUADRIENIO == @q')
        disc_zero = len(df_d.query('AMOUNT == 0'))
        E = (len(df_d) - disc_zero)
        F = len(df_d)
        G = df_d['AMOUNT'].sum()
        indaut = E / F
        indis = G / F
        # print(indaut, '--', indis, '--', disc_zero, F)
        ls_indautdisc_quad.append(q)
        ls_indautdisc.append(indaut)
        ls_indis.append(indis)
    df_indiscente = pd.DataFrame(list(zip(ls_indautdisc_quad,
                                          ls_indautdisc,
                                          ls_indis)),
                                 columns=['QUADRIENIO', 'INDOUT',
                                          'INDIS'])
    pathfilename = str('./csv_producao/' + 'capesindex_indautdis'  '.csv')
    df_indiscente.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_indiscente), ' quadrienios')


def capes_distindproddp():
    # lendo pesquisadores
    df_idlist = readIdList()
    num_dp = len(df_idlist)
    # lendo periodicos_uniq
    df = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                     header=0, sep=',')
    num_period_tot = len(df['QUALIS'])
    df.query('QUALIS != "XX"', inplace=True)
    df.query('QUALIS != "C "', inplace=True)
    df['YEAR'] = df['YEAR'].apply(iint)
    num_period_semqualis = num_period_tot - len(df['QUALIS'])
    print('Numero de periodicos sem QUALIS = ', num_period_semqualis)
    # definindo os quadrienios
    year_fquadrien = 2013
    ls_quadri = [year_fquadrien]
    for i in range(5):
        year_fquadrien = year_fquadrien + 4
        ls_quadri.append(year_fquadrien)
        # print(ls_quadri)
    # calculo para cada trienio
    ls_yini_quad = []
    ls_yfin_quad = []
    df_indprodart_full = pd.DataFrame(columns=['QUADRIENIO',
                                               'FULL_NAME',
                                               'INDPRODART',
                                               'CLASSIF'])
    for i in range(len(ls_quadri)):
        yini = ls_quadri[i]
        yfin = ls_quadri[i] + 3
        df_qtdby_qualis = df.groupby(['YEAR', 'FULL_NAME',
                                      'QUALIS'])['TITLE'].count().reset_index()
        df_qtdby_qualis.columns = ['YEAR', 'FULL_NAME', 'QUALIS', 'AMOUNT']
        # print(df_qtdby_qualis)
        df_qtdby_qualis.query('YEAR >= @yini and YEAR <= @yfin', inplace=True)
        if len(df_qtdby_qualis) < 1:
            pass
        else:
            # print('Quadrienio', yini, ' - ', yfin)
            df_qtdby_qualis['PESO'] = df_qtdby_qualis['QUALIS'].apply(
                fun_indprodart_classif)
            df_qtdby_qualis['PROD_AMOUPESO'] = df_qtdby_qualis['AMOUNT'] * \
                df_qtdby_qualis['PESO']
            # verificando representatividade B4 e B5 deve ser <= 0.2 por ano
            # print(df_qtdby_qualis)
            df_grade_tot_year = df_qtdby_qualis.groupby(
                ['YEAR'])['PROD_AMOUPESO'].sum().reset_index()
            df_qtdby_qualis_b4b5 = df_qtdby_qualis.query(
                'QUALIS == "B4" or QUALIS == "B5"')
            # print(df_grade_tot_year)
            # print(df_qtdby_qualis_b4b5)
            ls_years_b4b5_uniq = df_qtdby_qualis_b4b5['YEAR'].unique()
            for ia in range(len(ls_years_b4b5_uniq)):
                year_b4b5 = ls_years_b4b5_uniq[ia]
                df_yearb4b5 = df_qtdby_qualis_b4b5.query('YEAR == @year_b4b5')
                grade_tot_year_b4b5 = df_yearb4b5['PROD_AMOUPESO'].sum()
                df_temp = df_grade_tot_year.query('YEAR == @year_b4b5')
                grade_tot_year = df_temp['PROD_AMOUPESO'].sum()
                # print('Ano ', str(year_b4b5), 'B4 e B5 representam: ',
                #       str(round(grade_tot_year_b4b5 / grade_tot_year, 2)))
                if grade_tot_year_b4b5 / grade_tot_year > 0.2:
                    print('Para o ano ', str(year_b4b5),
                          'artigos B4 B5 glosados, maior que 0.2')
                    df_qtdby_qualis.query(
                        'YEAR != @year_b4b5 and QUALIS != "B4"', inplace=True)
                    df_qtdby_qualis.query(
                        'YEAR != @year_b4b5 and QUALIS != "B5"', inplace=True)
            df_qtdby_qualis = df_qtdby_qualis.groupby(
                ['YEAR', 'FULL_NAME'])['PROD_AMOUPESO'].sum() / num_dp
            df_qtdby_qualis = df_qtdby_qualis.reset_index()
            df_qtdby_qualis.columns = ['YEAR', 'FULL_NAME', 'INDPRODART']
            df_qtdby_qualis = df_qtdby_qualis.groupby(
                ['FULL_NAME'])['INDPRODART'].mean().reset_index()
            df_qtdby_qualis['CLASSIF'] = df_qtdby_qualis['INDPRODART'].apply(
                fun_indori_classif)
            quadr = str(str(yini) + '-' + str(yfin))
            df_qtdby_qualis['QUADRIENIO'] = np.repeat(
                quadr, len(df_qtdby_qualis))
            df_qtdby_qualis = df_qtdby_qualis[[
                'QUADRIENIO', 'FULL_NAME', 'INDPRODART', 'CLASSIF']]
            df_indprodart_full = pd.concat(
                [df_indprodart_full, df_qtdby_qualis], axis=0)
    pathfilename = str('./csv_producao/' + 'capesindex_distindproddp_doce.csv')
    df_indprodart_full.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(
        df_indprodart_full), ' pesquisadores para todos os quadrienios')
    # qd = df_indprodart_full['QUADRIENIO'].unique()
    df_distindproddp = df_indprodart_full.groupby(['QUADRIENIO', 'CLASSIF'])[
        'FULL_NAME'].count().reset_index()
    df_distindproddp.columns = ['QUADRIENIO', 'CLASSIF', 'COUNT']
    df_distindproddp['DISTINDPRODDP'] = 100 * \
        df_distindproddp['COUNT'] / num_dp
    df_distindproddp.query('CLASSIF != "FRACO" and CLASSIF != \
                           "DEFICIENTE"', inplace=True)
    df_distindproddp = df_distindproddp.groupby(
        ['QUADRIENIO'])['DISTINDPRODDP'].sum().reset_index()
    pathfilename = str('./csv_producao/' + 'capesindex_distindproddp'  '.csv')
    df_distindproddp.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(
        df_distindproddp), ' quadrienios')
