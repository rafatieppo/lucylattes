# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile

# ------------------------------------------------------------
# projetos de pesquisa institucionalizados / FAP
# ------------------------------------------------------------


def getprojpesqext(zipname):
    # lendo do zipfile
    zipfilepath = './xlm_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
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
                # print(cc)
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
                        # print(ls_allintproj)
                        # print(ls_allcoordsn)
                ls_intproj.append(ls_allintproj)
                ls_coord_sn.append(ls_allcoordsn)
    # DataFrame para os dados
    df_ppe = pd.DataFrame({'PROJ': ls_proj,
                           'YEAR_INI': ls_yini,
                           'YEAR_FIN': ls_yfin,
                           'NATUREZA': ls_natu,
                           'INTEGRANTES': ls_intproj,
                           'COORDENA': ls_coord_sn})
    latid = zipname.split('.')[0]
    pathfilename = str('./csv_ppe/' + latid + '_ppe'  '.csv')
    df_ppe.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_ppe['PROJ']), ' projetos')


# ------------------------------------------------------------
# iniciando funcao para producao tecnica do pesquisador - cursos etc
# ------------------------------------------------------------


def getprodtec(zipname):
    # lendo do zipfile
    zipfilepath = './xlm_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
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
            # print(cc)
            # definindo o ano do curso
            curso = str(ccdm[j])
            result = re.search('ano=\"(.*)\" doi',
                               curso)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
            ls_curscd_year.append(cc)
            # print(cc)
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
            # print(ls_all_autor)
            ls_curscd_integ.append(ls_all_autor)
    # DataFrame para cursos de curta duracao
    df_ccd = pd.DataFrame({'COURSE': ls_curscd_name,
                           'YEAR': ls_curscd_year,
                           'INTEGRANTES': ls_curscd_integ})
    latid = zipname.split('.')[0]
    pathfilename = str('./csv_ccd/' + latid + '_ccd'  '.csv')
    df_ccd.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_ccd['COURSE']), ' cursos')

# ------------------------------------------------------------
# iniciando funcao para orientacoes do pesquisador
# ------------------------------------------------------------


def getorient(zipname):
    # lendo do zipfile
    zipfilepath = './xlm_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
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
        # print(cc)
        # natureza da orientacao
        result = re.search('natureza=\"(.*)\" pais',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_nat.append(cc)
        # print(cc)
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
        # print(cc)
        # nome do curso
        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_curso.append(cc)
        # print(cc)
        # nome orientado
        result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_student.append(cc)
        # print(cc)
        # tipo de orientacao
        result = re.search('tipo-de-orientacao=\"(.*)\">',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_type.append(cc)
        # print(cc)
        # Bolsa
        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_suppo.append(cc)
        # print(cc)
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
        # print(cc)
        # natureza da orientacao
        result = re.search('natureza=\"(.*)\" pais',
                           dadobasico)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_nat.append(cc)
        # print(cc)
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
        # print(cc)
        # nome do curso
        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_curso.append(cc)
        # print(cc)
        # nome orientado
        result = re.search('nome-do-orientado=\"(.*)\" numero-de-paginas',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_student.append(cc)
        # print(cc)
        # tipo de orientacao
        result = re.search('tipo-de-orientacao-concluida=\"(.*)\">',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_type.append(cc)
        # print(cc)
        # Bolsa
        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                           detalhe)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_adv_suppo.append(cc)
        # print(cc)
    # DataFrame orientacoes
    df_advis = pd.DataFrame({'YEAR': ls_adv_year,
                             'NATURE': ls_adv_nat,
                             'INSTITUTION': ls_adv_inst,
                             'COURSE': ls_adv_curso,
                             'STUDENT': ls_adv_student,
                             'TYPE': ls_adv_type,
                             'SPONSOR': ls_adv_suppo})
    latid = zipname.split('.')[0]
    pathfilename = str('./csv_orientacoes/' + latid + '_advis'  '.csv')
    df_advis.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(df_advis['YEAR']), ' orientações')

# ------------------------------------------------------------
# Periodicos
# ------------------------------------------------------------


def getperiod(zipname):
    # lendo do zipfile
    # zipname = '3275865819287843.zip'
    zipfilepath = './xlm_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # extrair todas as producoes bibliograficas
    pb = soup.find_all('producao-bibliografica')
    len(pb)
    # listas para armazenamento de dados PERIODICOS
    ls_per_title = []
    ls_per_year = []
    ls_per_doi = []
    ls_per_lang = []
    ls_per_journal = []
    ls_per_issn = []
    ls_per_qualis = []
    ls_per_authors = []
    ls_per_authororder = []
    # Da producao bibliografica extrair o grupo de artigos publicados
    artspubs = pb[0].find_all('artigos-publicados')
    len(artspubs)
    # A partir do grupo de artigos publicados extrair os artigos
    # publicados
    artpub = artspubs[0].find_all('artigo-publicado')
    len(artpub)
    # a partir de cada artigo publicado extrair inf de interesse
    for i in range(len(artpub)):
        # dados basicos do paper
        dba = artpub[i].find_all('dados-basicos-do-artigo')
        paperdb = str(dba)
        # definindo o nome do paper
        result = re.search('titulo-do-artigo=\"(.*)\" titulo-do-artigo-i',
                           paperdb)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_per_title.append(cc)
        # print(cc)
        # definindo ano do paper
        result = re.search('ano-do-artigo=\"(.*)\" doi',
                           paperdb)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_per_year.append(cc)
        # print(cc)
        # definindo doi do paper
        result = re.search('doi=\"(.*)\" flag-divulgacao-c',
                           paperdb)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_per_doi.append(cc)
        # print(cc)
        # definindo idioma do paper
        result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                           paperdb)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_per_lang.append(cc)
        # print(cc)
        # detalhamento do paper
        dda = artpub[i].find_all('detalhamento-do-artigo')
        paperdt = str(dda)
        # definindo titulo do periodico
        result = re.search('titulo-do-periodico-ou-revista=\"(.*)\" volume',
                           paperdt)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
        ls_per_journal.append(cc)
        # print(cc)
        # definindo issn
        result = re.search('issn=\"(.*)\" local-de-public',
                           paperdt)
        if result is None:
            cc = 'VAZIO'
        else:
            cc = result.group(1)
            cc = str(cc[0:4]) + '-' + str(cc[4:])
        ls_per_issn.append(cc)
        # print(cc)
        # autores do paper
        aut = artpub[i].find_all('autores')
        ls_allauthors = []
        ls_allauthororder = []
        for j in range(len(aut)):
            auth = str(aut[j])
            result = re.search(
                'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                auth)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
            ls_allauthors.append(cc)
            # print(cc)
            # order de autoria
            result = re.search(
                'ordem-de-autoria=\"(.*)\"',
                auth)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
            ls_allauthororder.append(cc)
            # print(cc)
        ls_per_authors.append(ls_allauthors)
        ls_per_authororder.append(ls_allauthororder)
    # Qualis file
    config_file = open('./config.txt', 'r')
    qf = config_file.readlines()[4].split(':')[1]
    qf = qf.rstrip('\n')
    qf = qf.strip(' ')
    config_file.close()
    df_qualis = pd.read_csv(qf,
                            header=0, sep='\t')
    for k in range(len(ls_per_issn)):
        result = df_qualis[df_qualis['ISSN']
                           == ls_per_issn[k]].reset_index(drop=True)
        if len(result) == 0:
            cc = 'VAZIO'
        else:
            cc = result.iloc[0, 2]
        ls_per_qualis.append(cc)
        # print(cc)
    # DataFrame periodicos
    df_papers = pd.DataFrame({'TITLE': ls_per_title,
                              'YEAR': ls_per_year,
                              'DOI': ls_per_doi,
                              'LANG': ls_per_lang,
                              'JOURNAL': ls_per_journal,
                              'QUALIS': ls_per_qualis,
                              'ISSN': ls_per_issn,
                              'AUTHOR': ls_per_authors,
                              'ORDER': ls_per_authororder})
    latid = zipname.split('.')[0]
    pathfilename = str('./csv_periodicos/' + latid + '_period'  '.csv')
    df_papers.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com', len(
        df_papers['YEAR']), 'publicações em periódicos')
