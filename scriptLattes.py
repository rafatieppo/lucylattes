# ======================================================================
# Rafael Tieppo
# rafaeltieppo@yahoo.com.br
# https://rafatieppo.github.io/
# 16-01-2019
# LATTES Scraper
# ======================================================================

# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile

# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.style as style
# style.available
# style.use('fivethirtyeight')
# sns.set_style('whitegrid')

# ------------------------------------------------------------
# lendo a lista dos IDs e nome dos pesquisadores
from readidlist import readIdList
df_idlist = readIdList()
df_idlist
len(df_idlist)

# ------------------------------------------------------------
# lendo o arquivo ZIP

from parserlattes import getprojpesqext

for nid in range(len(df_idlist)):
    zipfilename = str(df_idlist.iloc[nid, 0]) + '.zip'
    getprojpesqext(zipfilename)


# ------------------------------------------------------------
# lendo arquivo gerado pelo script lattes
# ------------------------------------------------------------
# os.listdir('.')
# infile = open("./curriculo.xml", "r", encoding='ISO-8859-1')
# infile = open("./curriculo_riva.xml", "r", encoding='ISO-8859-1')
# contents = infile.read()
# soup = BeautifulSoup(contents, 'lxml')


def getprodtec():
    # extrair demais-tipos-de-producao-tecnica
    dtpt = soup.find_all('demais-tipos-de-producao-tecnica')
    # listas para armazenamento de dados producao tecnica
    ls_curscd_name = []
    ls_curscd_year = []
    ls_curscd_integ = []
    # A partir dos demais tipos de producao tecnica extrai-se os cursos,
    # palestras, etc
    for i in range(len(dtpt)):
        ccdm = dtpt[i].find_all('curso-de-curta-duracao-ministrado')
        for j in range(len(ccdm)):
            # definindo o nome do curso
            curso = str(ccdm[j])
            result = re.search('titulo=\"(.*)\" titulo-ingl',
                               curso)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
            ls_curscd_name.append(cc)
            print(cc)
            # definindo o ano do curso
            curso = str(ccdm[j])
            result = re.search('ano=\"(.*)\" doi',
                               curso)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
            ls_curscd_year.append(cc)
            print(cc)
            # Integrante do curso
            ccdm_aut = ccdm[j].find_all('autores')
            ls_all_autor = []
            for k in range(len(ccdm_aut)):
                autor = str(ccdm_aut[k])
                result = re.search(
                    'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                    autor)
                if result is None:
                    cc = 'VAZIO'
                else:
                    cc = result.group(1)
                ls_all_autor.append(cc)
            print(ls_all_autor)
            ls_curscd_integ.append(ls_all_autor)


# DataFrame para cursos de curta duracao
df_ccd = pd.DataFrame({'COURSE': ls_curscd_name,
                       'YEAR': ls_curscd_year,
                       'INTEGRANTES': ls_curscd_integ})
# df_ccd.to_csv('temp1.csv', index=False)


# ------------------------------------------------------------
# iniciando funcao para orientacoes do pesquisador
# ------------------------------------------------------------


def getorient():
    # extrair outras producoes
    op = soup.find_all('outra-producao')
    # listas para armazenamento de dados producao tecnica
    ls_adv_year = []
    ls_adv_nat = []
    ls_adv_inst = []
    ls_adv_curso = []
    ls_adv_student = []
    ls_adv_type = []
    ls_adv_suppo = []
    # extrair orientacoes concluidas Mestrado e Doutorado*
    orienconc = op[0].find_all('orientacoes-concluidas')
    # extrair orientacoes-concluidas-para-mestrado
    orienconc_mest = orienconc[0].find_all(
        'orientacoes-concluidas-para-mestrado')
    for i in range(len(orienconc_mest)):
        # definindo o nome do curso
        dadobasico = orienconc_mest[i].find_all(
            'dados-basicos-de-orientacoes-concluidas-para-mestrado')
        dadobasico = str(dadobasico)
        # ano da orientacao
        result = re.search('ano=\"(.*)\" doi',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_year.append(cc)
        print(cc)
        # natureza da orientacao
        result = re.search('natureza=\"(.*)\" pais',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_nat.append(cc)
        print(cc)
        # detalhes da orientacao ###
        detalhe = orienconc_mest[i].find_all(
            'detalhamento-de-orientacoes-concluidas-para-mestrado')
        detalhe = str(detalhe)
        # instituicao da orientacao
        result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_inst.append(cc)
        print(cc)
        # nome do curso
        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_curso.append(cc)
        print(cc)
        # nome orientado
        result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_student.append(cc)
        print(cc)
        # tipo de orientacao
        result = re.search('tipo-de-orientacao=\"(.*)\">',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_type.append(cc)
        print(cc)
        # Bolsa
        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_suppo.append(cc)
        print(cc)
    # outras orientacoes concluidas
    orienconc_out = op[0].find_all('outras-orientacoes-concluidas')
    for j in range(len(orienconc_out)):
        dadobasico = orienconc_out[j].find_all(
            'dados-basicos-de-outras-orientacoes-concluidas')
        dadobasico = str(dadobasico)
        # ano da orientacao
        result = re.search('ano=\"(.*)\" doi',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_year.append(cc)
        print(cc)
        # natureza da orientacao
        result = re.search('natureza=\"(.*)\" pais',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_nat.append(cc)
        print(cc)
        # detalhes da orientacao ######
        detalhe = orienconc_out[j].find_all(
            'detalhamento-de-outras-orientacoes-concluidas')
        detalhe = str(detalhe)
        # instituicao da orientacao
        result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_inst.append(cc)
        print(cc)
        # nome do curso
        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_curso.append(cc)
        print(cc)
        # nome orientado
        result = re.search('nome-do-orientado=\"(.*)\" numero-de-paginas',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_student.append(cc)
        print(cc)
        # tipo de orientacao
        result = re.search('tipo-de-orientacao-concluida=\"(.*)\">',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_type.append(cc)
        print(cc)
        # Bolsa
        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_suppo.append(cc)
        print(cc)


# DataFrame orientacoes
df_advis = pd.DataFrame({'YEAR': ls_adv_year,
                         'NATURE': ls_adv_nat,
                         'INTITUTION': ls_adv_inst,
                         'COURSE': ls_adv_curso,
                         'STUDENT': ls_adv_student,
                         'TYPE': ls_adv_type,
                         'SPONSOR': ls_adv_suppo})
# df_advis.to_csv('temp3.csv', index=False)
