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
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.style as style
import os
# style.available
# style.use('fivethirtyeight')
# sns.set_style('whitegrid')
import requests
from bs4 import BeautifulSoup
import re

# ------------------------------------------------------------
# lendo arquivo gerado pelo script lattes
# ------------------------------------------------------------
os.listdir('.')
infile = open("./curriculo.xml", "r", encoding='ISO-8859-1')
infile = open("./curriculo_riva.xml", "r", encoding='ISO-8859-1')
contents = infile.read()
soup = BeautifulSoup(contents, 'lxml')

# ------------------------------------------------------------
# projetos de pesquisa institucionalizados / FAP
# ------------------------------------------------------------


def getprojpesqext():
    # extrair todas as atividades profissionais
    ap = soup.find_all('atuacao-profissional')
    len(ap)
    # listas para armazenamento de dados PROJETOS PESQ e EXT
    ls_coord_sn = []
    ls_intproj = []
    ls_natu = []
    ls_proj = []
    ls_yfin = []
    ls_yini = []
    # A partir das atividades profissionais, para cada uma delas (Unioeste,
    # DGF, etc) há diversas atividades, contudo queremos a participação em
    # projetos. No caso pegamos o ap é 5 que é da unemat.
    for i in range(len(ap)):
        app = ap[i].find_all('atividades-de-participacao-em-projeto')
        # a partir das atividades de participacao em projeto, filtra-se todos os
        # projeto de pesquisa que contem os projetos de ext e pesq que ocorreu
        # na instituicao
        for j in range(len(app)):
            ppe = app[j].find_all('projeto-de-pesquisa')
            # definindo o nome do projeto
            for k in range(len(ppe)):
                proj = str(ppe[k])
                result = re.search('nome-do-projeto=\"(.*)\" nome-do-projeto-i',
                                   proj)
                if result is None:
                    cc = 'VAZIO'
                else:
                    cc = result.group(1)
                ls_proj.append(cc)
                print(cc)
                # definindo o ano inicial
                # result = re.search('ano-inicio=\"(.*)\" data-certificacao', proj)
                result = re.search('ano-inicio="(.*)" da',
                                   proj)
                if result is None:
                    cc = 'VAZIO'
                else:
                    cc = result.group(1)
                ls_yini.append(cc)
                # definindo o ano final
                result = re.search('ano-fim="(.*)" ano-inicio',
                                   proj)
                if result is None:
                    cc = 'VAZIO'
                else:
                    cc = result.group(1)
                if cc == '':
                    cc = 'ATUAL'
                ls_yfin.append(cc)
                # definindo a natureza
                result = re.search('natureza=\"(.*)\" nome-coordenador', proj)
                if result is None:
                    cc = 'VAZIO'
                else:
                    cc = result.group(1)
                ls_natu.append(cc)
                # Integrante do projeto
                ep = ppe[k].find_all('equipe-do-projeto')
                for m in range(len(ep)):
                    ip = ep[m].find_all('integrantes-do-projeto')
                    ls_allintproj = []
                    ls_allcoordsn = []
                    for m in range(len(ip)):
                        integ = str(ip[m])
                        result = re.search(
                            'nome-completo=\"(.*)\" nome-para-citacao',
                            integ)
                        if result is None:
                            cc = 'VAZIO'
                        else:
                            cc = result.group(1)
                        ls_allintproj.append(cc)
                # definindo se é coordenador SIM ou NAO
                        result = re.search(
                            'responsavel=\"(.*)\" nome-completo', integ)
                        if result is None:
                            cc = 'VAZIO'
                        else:
                            cc = result.group(1)
                        ls_allcoordsn.append(cc)
                        print(ls_allintproj)
                        print(ls_allcoordsn)
                ls_intproj.append(ls_allintproj)
                ls_coord_sn.append(ls_allcoordsn)


# DataFrame para os dados
df_ppe = pd.DataFrame({'PROJ': ls_proj,
                       'YEAR_INI': ls_yini,
                       'YEAR_FIN': ls_yfin,
                       'NATUREZA': ls_natu,
                       'INTEGRANTES': ls_intproj,
                       'COORDENA': ls_coord_sn})
#df_ppe.to_csv('temp.csv', index=False)
df_ppe.shape


# ------------------------------------------------------------
# iniciando funcao para producao tecnica do pesquisador - cursos etc
# ------------------------------------------------------------


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
