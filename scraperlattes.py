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
from extrafuns import fun_result
# ------------------------------------------------------------
# ------------------------------------------------------------
# projetos de pesquisa institucionalizados / FAP
# ------------------------------------------------------------


def getprojpesqext(zipname):
    # lendo do zipfile
    # zipname = '3275865819287843.zip'
    # zipname = '8190371175828378.zip'
    # zipname = '5859946324646438.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # ttfile = open('tt.xml', 'w')
    # ttfile.write(soup.prettify())
    # ttfile.close()
    # extrair todas as atividades profissionais
    ap = soup.find_all('atuacao-profissional')
    # VERIFICANDO se ha atuacao profissional
    if len(ap) == 0:
        print('Atuacao profissional nao encontrada para', zipname)
    else:
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
            # VERIFICANDO se ha participacao em projeto
            if len(app) == 0:
                print(
                    'Participacao em projeto em uma das atividades profissionais nao encontrada para', zipname)
            else:
                for j in range(len(app)):
                    ppe = app[j].find_all('projeto-de-pesquisa')
                    # definindo o nome do projeto
                    for k in range(len(ppe)):
                        proj = str(ppe[k])
                        result = re.search('nome-do-projeto=\"(.*)\" nome-do-projeto-i',
                                           proj)
                        cc = fun_result(result)
                        ls_proj.append(cc)
                        # print(cc)
                        # definindo o ano inicial
                        # result = re.search('ano-inicio=\"(.*)\" data-certificacao', proj)
                        result = re.search('ano-inicio="(.*)" data-certificacao',
                                           proj)
                        cc = fun_result(result)
                        ls_yini.append(cc)
                        # definindo o ano final
                        result = re.search('ano-fim="(.*)" ano-inicio',
                                           proj)
                        cc = fun_result(result)
                        if result is None:
                            cc = 'VAZIO'
                        else:
                            cc = result.group(1)
                        if cc == '':
                            cc = 'ATUAL'
                        ls_yfin.append(cc)
                        # definindo a natureza
                        result = re.search(
                            'natureza=\"(.*)\" nome-coordenador', proj)
                        cc = fun_result(result)
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
                                cc = fun_result(result)
                                ls_allintproj.append(cc)
                        # definindo se é coordenador SIM ou NAO
                                result = re.search(
                                    'responsavel=\"(.*)\" nome-completo', integ)
                                cc = fun_result(result)
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
        pathfilename = str('./csv_producao/' + latid + '_ppe'  '.csv')
        df_ppe.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(df_ppe['PROJ']), ' projetos')


# ------------------------------------------------------------
# iniciando funcao para producao tecnica do pesquisador - cursos etc
# ------------------------------------------------------------


def getprodtec(zipname):
    # lendo do zipfile
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # extrair demais-tipos-de-producao-tecnica
    dtpt = soup.find_all('demais-tipos-de-producao-tecnica')
    # VERIFICANDO se ha demais tipos de producao
    if len(dtpt) == 0:
        print('Demais tipos de producao nao encontrada para', zipname)
    else:
        # listas para armazenamento de dados producao tecnica
        ls_curscd_name = []
        ls_curscd_year = []
        ls_curscd_integ = []
        # A partir dos demais tipos de producao tecnica extrai-se os cursos,
        # palestras, etc
        for i in range(len(dtpt)):
            ccdm = dtpt[i].find_all('curso-de-curta-duracao-ministrado')
            # VERIFICANDO se ha cursos
            if len(ccdm) == 0:
                print('Curso de cura duracao nao encontrado para', zipname)
            else:
                for j in range(len(ccdm)):
                    # definindo o nome do curso
                    curso = str(ccdm[j])
                    result = re.search('titulo=\"(.*)\" titulo-ingl',
                                       curso)
                    cc = fun_result(result)
                    ls_curscd_name.append(cc)
                    # print(cc)
                    # definindo o ano do curso
                    curso = str(ccdm[j])
                    result = re.search('ano=\"(.*)\" doi',
                                       curso)
                    cc = fun_result(result)
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
                        cc = fun_result(result)
                        ls_all_autor.append(cc)
                    # print(ls_all_autor)
                    ls_curscd_integ.append(ls_all_autor)
        # DataFrame para cursos de curta duracao
        df_ccd = pd.DataFrame({'COURSE': ls_curscd_name,
                               'YEAR': ls_curscd_year,
                               'INTEGRANTES': ls_curscd_integ})
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_ccd'  '.csv')
        df_ccd.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(df_ccd['COURSE']), ' cursos')

# ------------------------------------------------------------
# iniciando funcao para orientacoes do pesquisador
# ------------------------------------------------------------


def getorient(zipname):
    # lendo do zipfile
    # zipname = '1292986021348016.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # extrair outras producoes
    op = soup.find_all('outra-producao')
    # VERIFICANDO se ha outra producao
    if len(op) == 0:
        print('Outras producoes nao encontradas para', zipname)
    else:
        # extrair orientacoes concluidas Mestrado e Doutorado*
        orienconc = op[0].find_all('orientacoes-concluidas')
        # VERIFICANDO se ha orientacoes pos
        if len(orienconc) == 0:
            print('Orientacoes nao encontradas para', zipname)
        else:
            # listas para armazenamento de dados producao tecnica
            ls_adv_year = []
            ls_adv_nat = []
            ls_adv_inst = []
            ls_adv_curso = []
            ls_adv_student = []
            ls_adv_type = []
            ls_adv_suppo = []
            # extrair orientacoes-concluidas-para-mestrado
            orienconc_mest = orienconc[0].find_all(
                'orientacoes-concluidas-para-mestrado')
            # VERIFICANDO se ha orientacoes mestrado e doutorado
            if len(orienconc_mest) == 0:
                print('Orientacoes concluidas de mestrado nao encontradas para', zipname)
            else:
                for i in range(len(orienconc_mest)):
                    # definindo o nome do curso
                    dadobasico = orienconc_mest[i].find_all(
                        'dados-basicos-de-orientacoes-concluidas-para-mestrado')
                    dadobasico = str(dadobasico)
                    # ano da orientacao
                    result = re.search('ano=\"(.*)\" doi',
                                       dadobasico)
                    cc = fun_result(result)
                    ls_adv_year.append(cc)
                    # print(cc)
                    # natureza da orientacao
                    result = re.search('natureza=\"(.*)\" pais',
                                       dadobasico)
                    cc = fun_result(result)
                    ls_adv_nat.append(cc)
                    # print(cc)
                    # detalhes da orientacao ###
                    detalhe = orienconc_mest[i].find_all(
                        'detalhamento-de-orientacoes-concluidas-para-mestrado')
                    detalhe = str(detalhe)
                    # instituicao da orientacao
                    result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_inst.append(cc)
                    # print(cc)
                    # nome do curso
                    result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_curso.append(cc)
                    # print(cc)
                    # nome orientado
                    result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_student.append(cc)
                    # print(cc)
                    # tipo de orientacao
                    result = re.search('tipo-de-orientacao=\"(.*)\">',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_type.append(cc)
                    # print(cc)
                    # Bolsa
                    result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_suppo.append(cc)
                    # print(cc)
            # ------------------------------------------------------------
            # extrair orientacoes-concluidas-para-doutorado
            orienconc_dout = orienconc[0].find_all(
                'orientacoes-concluidas-para-doutorado')
            # VERIFICANDO se ha orientacoes  doutorado
            if len(orienconc_dout) == 0:
                print(
                    'Orientacoes concluidas de doutorado nao encontradas para', zipname)
            else:
                for i in range(len(orienconc_dout)):
                    # definindo o nome do curso
                    dadobasico = orienconc_dout[i].find_all(
                        'dados-basicos-de-orientacoes-concluidas-para-doutorado')
                    dadobasico = str(dadobasico)
                    # ano da orientacao
                    result = re.search('ano=\"(.*)\" doi',
                                       dadobasico)
                    cc = fun_result(result)
                    ls_adv_year.append(cc)
                    # print(cc)
                    # natureza da orientacao
                    result = re.search('natureza=\"(.*)\" pais',
                                       dadobasico)
                    cc = fun_result(result)
                    ls_adv_nat.append(cc)
                    # print(cc)
                    # detalhes da orientacao ###
                    detalhe = orienconc_dout[i].find_all(
                        'detalhamento-de-orientacoes-concluidas-para-doutorado')
                    detalhe = str(detalhe)
                    # instituicao da orientacao
                    result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_inst.append(cc)
                    # print(cc)
                    # nome do curso
                    result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_curso.append(cc)
                    # print(cc)
                    # nome orientado
                    result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_student.append(cc)
                    # print(cc)
                    # tipo de orientacao
                    result = re.search('tipo-de-orientacao=\"(.*)\">',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_type.append(cc)
                    # print(cc)
                    # Bolsa
                    result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                       detalhe)
                    cc = fun_result(result)
                    ls_adv_suppo.append(cc)
                    # print(cc)
        # ------------------------------------------------------------
        # outras orientacoes concluidas
        orienconc_out = op[0].find_all('outras-orientacoes-concluidas')
        # VERIFICANDO se ha outras orientacoes pos
        if len(orienconc_out) == 0:
            print('Outras orientacoes nao encontradas para', zipname)
        else:
            for j in range(len(orienconc_out)):
                dadobasico = orienconc_out[j].find_all(
                    'dados-basicos-de-outras-orientacoes-concluidas')
                dadobasico = str(dadobasico)
                # ano da orientacao
                result = re.search('ano=\"(.*)\" doi',
                                   dadobasico)
                cc = fun_result(result)
                ls_adv_year.append(cc)
                # print(cc)
                # natureza da orientacao
                result = re.search('natureza=\"(.*)\" pais',
                                   dadobasico)
                cc = fun_result(result)
                ls_adv_nat.append(cc)
                # print(cc)
                # detalhes da orientacao ######
                detalhe = orienconc_out[j].find_all(
                    'detalhamento-de-outras-orientacoes-concluidas')
                detalhe = str(detalhe)
                # instituicao da orientacao
                result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                   detalhe)
                cc = fun_result(result)
                ls_adv_inst.append(cc)
                # print(cc)
                # nome do curso
                result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                   detalhe)
                cc = fun_result(result)
                ls_adv_curso.append(cc)
                # print(cc)
                # nome orientado
                result = re.search('nome-do-orientado=\"(.*)\" numero-de-paginas',
                                   detalhe)
                cc = fun_result(result)
                ls_adv_student.append(cc)
                # print(cc)
                # tipo de orientacao
                result = re.search('tipo-de-orientacao-concluida=\"(.*)\">',
                                   detalhe)
                cc = fun_result(result)
                ls_adv_type.append(cc)
                # print(cc)
                # Bolsa
                result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                   detalhe)
                cc = fun_result(result)
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
            pathfilename = str('./csv_producao/' +
                               latid + '_advis'  '.csv')
            df_advis.to_csv(pathfilename, index=False)
            print(pathfilename, ' gravado com', len(
                df_advis['YEAR']), ' orientações')

# ------------------------------------------------------------
# Periodicos
# ------------------------------------------------------------


def getperiod(zipname):
    # lendo do zipfile
    #zipname = '3275865819287843.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # capturando nome completo para ordem de autoria
    cv = soup.find_all('curriculo-vitae')
    if len(cv) == 0:
        print('curriculo vitae nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados producao tecnica
        for i in range(len(cv)):
            dg = cv[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dg) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dg)):
                    # definindo nome completo
                    gendata = str(dg[j])
                    result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                       gendata)
                    cc = fun_result(result)
                    fullname = cc
    # ------------------------------------------------------------
    # extrair todas as producoes bibliograficas
    pb = soup.find_all('producao-bibliografica')
    # VERIFICANDO se ha demais tipos de producao
    if len(pb) == 0:
        print('Producoes bibliograficas nao encontradas para', zipname)
    else:
        # Da producao bibliografica extrair o grupo de artigos publicados
        artspubs = pb[0].find_all('artigos-publicados')
        # VERIFICANDO se ha artigos publicados
        if len(artspubs) == 0:
            print('Artigos publicados nao encontrados para', zipname)
        else:
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
            ls_per_orders = []
            ls_jcr = []
            # A partir do grupo de artigos publicados extrair os artigos
            # publicados
            artpub = artspubs[0].find_all('artigo-publicado')
            # a partir de cada artigo publicado extrair inf de interesse
            for i in range(len(artpub)):
                # dados basicos do paper
                dba = artpub[i].find_all('dados-basicos-do-artigo')
                paperdb = str(dba)
                # definindo o nome do paper
                result = re.search('titulo-do-artigo=\"(.*)\" titulo-do-artigo-i',
                                   paperdb)
                cc = fun_result(result)
                ls_per_title.append(cc)
                # print(cc)
                # definindo ano do paper
                result = re.search('ano-do-artigo=\"(.*)\" doi',
                                   paperdb)
                cc = fun_result(result)
                ls_per_year.append(cc)
                # print(cc)
                # definindo doi do paper
                result = re.search('doi=\"(.*)\" flag-divulgacao-c',
                                   paperdb)
                cc = fun_result(result)
                ls_per_doi.append(cc)
                # print(cc)
                # definindo idioma do paper
                result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                   paperdb)
                cc = fun_result(result)
                ls_per_lang.append(cc)
                # print(cc)
                # detalhamento do paper
                dda = artpub[i].find_all('detalhamento-do-artigo')
                paperdt = str(dda)
                # definindo titulo do periodico
                result = re.search('titulo-do-periodico-ou-revista=\"(.*)\" volume',
                                   paperdt)
                cc = fun_result(result)
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
                ls_authororder = []
                for j in range(len(aut)):
                    auth = str(aut[j])
                    result = re.search(
                        'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                        auth)
                    if result is None:
                        cc = 'VAZIO'
                    else:
                        cc = result.group(1)
                        nca = result.group(1)  # nomecompletoautor
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
                        ncao = result.group(1)
                    ls_allauthororder.append(cc)
                    if fullname == nca:
                        ls_authororder.append(ncao)
                        # print(fullname + ' ' + ncao)
                    # print(cc)
                ls_per_authors.append(ls_allauthors)
                ls_per_authororder.append(ls_allauthororder)
                ls_per_orders.append(ls_authororder)
            # Qualis file
            config_file = open('./config.txt', 'r')
            # config_file = open('./config.txt', 'r', encoding='utf-8')
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
                    cc = 'XX'
                else:
                    cc = result.iloc[0, 2]
                ls_per_qualis.append(cc)
                # print(cc)
            # JCR
            df_jcr = pd.read_csv('jcr_factor.csv', sep=',',
                                 header=0, dtype='str')
            for k in range(len(ls_per_issn)):
                issnclean = str(ls_per_issn[k])
                issnclean = str(issnclean.replace('-', ''))
                result = df_jcr[df_jcr['ISSN_A']
                                == issnclean].reset_index(drop=True)
                if len(result) == 0:
                    result = df_jcr[df_jcr['ISSN_B']
                                    == issnclean].reset_index(drop=True)
                    if len(result) == 0:
                        cc = -99
                    else:
                        cc = result.iloc[0, 7]
                else:
                    cc = result.iloc[0, 7]
                ls_jcr.append(cc)
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
                                      'ORDER': ls_per_authororder,
                                      'ORDER_OK': ls_per_orders,
                                      'JCR': ls_jcr})
            latid = zipname.split('.')[0]
            pathfilename = str('./csv_producao/' + latid + '_period'  '.csv')
            df_papers.to_csv(pathfilename, index=False)
            print(pathfilename, ' gravado com', len(
                df_papers['YEAR']), 'publicações em periódicos')


# ------------------------------------------------------------
# Livros
# ------------------------------------------------------------


def getlivro(zipname):
    # lendo do zipfile
    # zipname = '1292986021348016.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # capturando nome completo para ordem de autoria
    cv = soup.find_all('curriculo-vitae')
    if len(cv) == 0:
        print('curriculo vitae nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados producao tecnica
        for i in range(len(cv)):
            dg = cv[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dg) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dg)):
                    # definindo nome completo
                    gendata = str(dg[j])
                    result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                       gendata)
                    cc = fun_result(result)
                    fullname = cc
    # ------------------------------------------------------------
    # extrair todas as producoes livros e capitulos
    livscaps = soup.find_all('livros-e-capitulos')
    # VERIFICANDO se ha livros e capitulos
    if len(livscaps) == 0:
        print('Livros publicados nao encontrados para', zipname)
    else:
        livspuborg = livscaps[0].find_all('livros-publicados-ou-organizados')
        # VERIFICANDO se ha livros publicados ou organizados
        if len(livspuborg) == 0:
            print('Livros publicados ou organizados nao encontrados para', zipname)
        else:
            livpuborg = livspuborg[0].find_all('livro-publicado-ou-organizado')
            # listas para armazenamento de dados livros e capitulos
            ls_liv_title = []
            ls_liv_year = []
            ls_liv_lang = []
            ls_liv_edit = []
            ls_liv_authors = []
            ls_liv_authororder = []
            ls_liv_orders = []
            # a partir de cada livro capitulo publicado extrair inf de interesse
            for i in range(len(livpuborg)):
                # dados basicos do livro
                dbl = livpuborg[i].find_all('dados-basicos-do-livro')
                livrodb = str(dbl)
                # definindo o nome do livro
                result = re.search('titulo-do-livro=\"(.*)\" titulo-do-livro-i',
                                   livrodb)
                cc = fun_result(result)
                ls_liv_title.append(cc)
                # print(cc)
                # definindo ano do livro
                result = re.search('ano=\"(.*)\" doi',
                                   livrodb)
                cc = fun_result(result)
                ls_liv_year.append(cc)
                # print(cc)
                # definindo idioma do livro
                result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                   livrodb)
                cc = fun_result(result)
                ls_liv_lang.append(cc)
                # detalhamento do livro
                ddl = livpuborg[i].find_all('detalhamento-do-livro')
                livrodt = str(ddl)
                # definindo editora
                result = re.search('nome-da-editora=\"(.*)\" volume',
                                   livrodt)
                cc = fun_result(result)
                ls_liv_edit.append(cc)
                # print(cc)
                # autores do livro
                aut = livpuborg[i].find_all('autores')
                ls_allauthors = []
                ls_allauthororder = []
                ls_authororder = []
                for j in range(len(aut)):
                    auth = str(aut[j])
                    result = re.search(
                        'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                        auth)
                    if result is None:
                        cc = 'VAZIO'
                    else:
                        cc = result.group(1)
                        nca = result.group(1)  # nomecompletoautor
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
                        ncao = result.group(1)
                    ls_allauthororder.append(cc)
                    if fullname == nca:
                        ls_authororder.append(ncao)
                        # print(fullname + ' ' + ncao)
                    # print(cc)
                ls_liv_authors.append(ls_allauthors)
                ls_liv_authororder.append(ls_allauthororder)
                ls_liv_orders.append(ls_authororder)
                # print(cc)
            # DataFrame livros publicados
            df_livro = pd.DataFrame({'TITLE': ls_liv_title,
                                     'YEAR': ls_liv_year,
                                     'LANG': ls_liv_lang,
                                     'EDITORA': ls_liv_edit,
                                     'AUTHOR': ls_liv_authors,
                                     'ORDER': ls_liv_authororder,
                                     'ORDER_OK': ls_liv_orders})
            latid = zipname.split('.')[0]
            pathfilename = str('./csv_producao/' + latid + '_livro'  '.csv')
            df_livro.to_csv(pathfilename, index=False)
            print(pathfilename, ' gravado com', len(
                df_livro['YEAR']), 'livros publicados')


# ------------------------------------------------------------
# Capitulos de livros
# ------------------------------------------------------------


def getcapit(zipname):
    # lendo do zipfile
    # zipname = '1292986021348016.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # capturando nome completo para ordem de autoria
    cv = soup.find_all('curriculo-vitae')
    if len(cv) == 0:
        print('curriculo vitae nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados producao tecnica
        for i in range(len(cv)):
            dg = cv[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dg) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dg)):
                    # definindo nome completo
                    gendata = str(dg[j])
                    result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                       gendata)
                    cc = fun_result(result)
                    fullname = cc
    # ------------------------------------------------------------
    # extrair todas as producoes livros e capitulos
    livscaps = soup.find_all('livros-e-capitulos')
    # VERIFICANDO se ha livros e capitulos
    if len(livscaps) == 0:
        print('Capitulos publicados nao encontrados para', zipname)
    else:
        capspuborg = livscaps[0].find_all('capitulos-de-livros-publicados')
        # VERIFICANDO se ha capitulos
        if len(capspuborg) == 0:
            print('Capitulos publicados nao encontrados para', zipname)
        else:
            cappuborg = capspuborg[0].find_all('capitulo-de-livro-publicado')
            # listas para armazenamento de dados livros e capitulos
            ls_cap_title = []
            ls_cap_year = []
            ls_cap_lang = []
            ls_cap_edit = []
            ls_cap_authors = []
            ls_cap_authororder = []
            ls_cap_orders = []
            # a partir de cada livro capitulo publicado extrair inf de interesse
            for i in range(len(cappuborg)):
                # dados basicos do livro
                dbc = cappuborg[i].find_all('dados-basicos-do-capitulo')
                capitdb = str(dbc)
                # definindo o nome do capitulo
                result = re.search(
                    'titulo-do-capitulo-do-livro=\"(.*)\" titulo-do-capi',
                    capitdb)
                cc = fun_result(result)
                ls_cap_title.append(cc)
                # print(cc)
                # definindo ano do livro
                result = re.search('ano=\"(.*)\" doi',
                                   capitdb)
                cc = fun_result(result)
                ls_cap_year.append(cc)
                # print(cc)
                # definindo idioma do livro
                result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                   capitdb)
                cc = fun_result(result)
                ls_cap_lang.append(cc)
                # detalhamento do livro
                ddc = cappuborg[i].find_all('detalhamento-do-capitulo')
                capitdt = str(ddc)
                # definindo editora
                result = re.search(
                    'nome-da-editora=\"(.*)\" numero-da-edicao-r',
                    capitdt)
                cc = fun_result(result)
                ls_cap_edit.append(cc)
                # print(cc)
                # autores do livro
                aut = cappuborg[i].find_all('autores')
                ls_allauthors = []
                ls_allauthororder = []
                ls_allorders = []
                ls_authororder = []
                for j in range(len(aut)):
                    auth = str(aut[j])
                    result = re.search(
                        'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                        auth)
                    if result is None:
                        cc = 'VAZIO'
                    else:
                        cc = result.group(1)
                        nca = result.group(1)  # nomecompletoautora
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
                        ncao = result.group(1)
                    ls_allauthororder.append(cc)
                    if fullname == nca:
                        ls_authororder.append(ncao)
                        # print(fullname + ' ' + ncao)
                    # print(cc)
                ls_cap_authors.append(ls_allauthors)
                ls_cap_authororder.append(ls_allauthororder)
                ls_cap_orders.append(ls_authororder)
                # print(cc)
            # DataFrame livros publicados
            df_capit = pd.DataFrame({'TITLE': ls_cap_title,
                                     'YEAR': ls_cap_year,
                                     'LANG': ls_cap_lang,
                                     'EDITORA': ls_cap_edit,
                                     'AUTHOR': ls_cap_authors,
                                     'ORDER': ls_cap_authororder,
                                     'ORDER_OK': ls_cap_orders})
            latid = zipname.split('.')[0]
            pathfilename = str('./csv_producao/' + latid + '_capitulo'  '.csv')
            df_capit.to_csv(pathfilename, index=False)
            print(pathfilename, ' gravado com', len(
                df_capit['YEAR']), 'capítulos publicados')


# ------------------------------------------------------------
# Nome completo, nome citacao, e bio
# ------------------------------------------------------------


def getnomecompleto(zipname):
    # lendo do zipfile
    # zipname = '3275865819287843.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # extrair curriculo vitae
    cv = soup.find_all('curriculo-vitae')
    # VERIFICANDO se ha demais tipos de producao
    if len(cv) == 0:
        print('curriculo vitae nao encontrado para', zipname)
    else:
        # listas para armazenamento de dados producao tecnica
        ls_name_full = []
        ls_name_last = []
        ls_name_id = []
        ls_city = []
        ls_state = []
        ls_citado = []
        ls_orcid = []
        ls_abstrac = []
        ls_update = []
        ls_address_enterp = []
        for i in range(len(cv)):
            # definindo atualizacao
            cvdata = str(cv[i])
            result = re.search('data-atualizacao=\"(.*)\" hora-atualizacao',
                               cvdata)
            if result is None:
                cc = 'VAZIO'
            else:
                cc = result.group(1)
                upd = str(cc[0:2]) + '-' + \
                    str(cc[2:4]) + '-' + str(cc[4:])
                cc = upd
                # print(cc)
                ls_update.append(cc)
            dg = cv[i].find_all('dados-gerais')
            # VERIFICANDO se ha dados gerais
            if len(dg) == 0:
                print('Dados gerais nao encontrados para', zipname)
            else:
                for j in range(len(dg)):
                    # definindo nome completo
                    gendata = str(dg[j])
                    result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                       gendata)
                    cc = fun_result(result)
                    ls_name_full.append(cc)
                    lastname = cc.split(' ')[-1]
                    ls_name_last.append(lastname)
                    idd = zipname.split('.')[0]
                    ls_name_id.append(idd)
                    # definindo cidade
                    gendata = str(dg[j])
                    result = re.search(
                        'cidade-nascimento=\"(.*)\" data-faleci',
                        gendata)
                    cc = fun_result(result)
                    ls_city.append(cc)
                    # definindo estado
                    gendata = str(dg[j])
                    result = re.search('uf-nascimento=\"(.*)\"><res',
                                       gendata)
                    cc = fun_result(result)
                    ls_state.append(cc)
                    # definindo nome em citacoes
                    gendata = str(dg[j])
                    result = re.search(
                        'nome-em-citacoes-bibliograficas=\"(.*)\" orcid-id',
                        gendata)
                    cc = fun_result(result)
                    ls_citado.append(cc)
                    # definindo ORCID
                    gendata = str(dg[j])
                    result = re.search('orcid-id=\"(.*)\" pais-de-nacionali',
                                       gendata)
                    cc = fun_result(result)
                    ls_orcid.append(cc)

            rescv = cv[i].find_all('resumo-cv')
            address = cv[i].find_all('endereco')
            # VERIFICANDO se ha resumo
            if len(rescv) == 0:
                print('Resumo cv nao encontrados para', zipname)
                cc = 'VAZIO'
                ls_abstrac.append(cc)
            else:
                for j in range(len(rescv)):
                    # definindo resumo
                    abstdata = str(rescv[j])
                    result = re.search('texto-resumo-cv-rh=\"(.*)\" texto-resumo-cv-rh-en=',
                                       abstdata, re.DOTALL)
                    if result is None:
                        cc = 'Nao foi possivel extrair o resumo'
                    else:
                        cc = result.group(1)
                    ls_abstrac.append(cc)
            # VERIFICANDO se ha endereco
            if len(address) == 0:
                print('Endereco nao encontrado para', zipname)
                cc = 'VAZIO'
                ls_address_enterp.append(cc)
            else:
                for j in range(len(address)):
                    # verificando se ha endereco profissional
                    address_prof = address[j].find_all('endereco-profissional')
                    if len(address_prof) == 0:
                        print('Endereco profissional nao encontrado para', zipname)
                        cc == 'VAZIO'
                        ls_address_enterp.append(cc)
                    else:
                        # definindo endereco
                        addressdata = str(address_prof[0])
                        result = re.search('nome-instituicao-empresa=\"(.*)\" nome-orgao=',
                                           addressdata, re.DOTALL)
                        if result is None:
                            cc = 'Nao foi possivel extrair o endereco profissional'
                        else:
                            cc = result.group(1)
                            ls_address_enterp.append(cc)
        # DataFrame nome completo e sobrenome
        df_fullname = pd.DataFrame({'ID': ls_name_id,
                                    'FULL_NAME': ls_name_full,
                                    'LAST_NAME': ls_name_last,
                                    'CITADO': ls_citado,
                                    'CITY': ls_city,
                                    'STATE': ls_state,
                                    'RESUME': ls_abstrac,
                                    'UPDATE': ls_update,
                                    'ADDRESS_ENTERP': ls_address_enterp,
                                    'ORCID': ls_orcid})
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_fullname'  '.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(df_fullname['ID']), 'nomes completos')


# ------------------------------------------------------------
# Disciplinas ministradas
# ------------------------------------------------------------


def getdiscip(zipname):
    # lendo do zipfile
    # zipname = '3275865819287843.zip'
    # zipname = '8190371175828378.zip'
    # zipname = '5859946324646438.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    # ttfile = open('tt.xml', 'w')
    # ttfile.write(soup.prettify())
    # ttfile.close()
    # extrair todas as atividades profissionais
    ap = soup.find_all('atuacao-profissional')
    # VERIFICANDO se ha atuacao profissional
    if len(ap) == 0:
        print('Atuacao profissional nao encontrada para', zipname)
    else:
        # listas para armazenamento de dados PROJETOS PESQ e EXT
        ls_inst = []
        ls_yini = []
        ls_yfin = []
        ls_mini = []
        ls_mfin = []
        ls_curs = []
        ls_tipo = []
        ls_disc = []
        for i in range(len(ap)):
            instit = re.search('nome-instituicao=\"(.*)\" sequencia-atividade',
                               str(ap[i]))
            instit = fun_result(instit)
            app = ap[i].find_all('atividades-de-ensino')
            # a partir das atividades de participacao em projeto, filtra-se todos os
            # projeto de pesquisa que contem os projetos de ext e pesq que ocorreu
            # na instituicao
            # VERIFICANDO se ha participacao em projeto
            if len(app) == 0:
                print(
                    'Atividades de ensino não encontrada para ', zipname)
            else:
                for j in range(len(app)):
                    ens = app[j].find_all('ensino')
                    if len(ens) == 0:
                        print(
                            'ensino não encontrado para ', zipname)
                    else:
                        for k in range(len(ens)):
                            # registrando instituicao
                            ls_inst.append(instit)
                            # definindo o ano ini
                            aten = str(ens[k])
                            result = re.search('ano-inicio=\"(.*)\" codigo-curso',
                                               aten)
                            cc = fun_result(result)
                            ls_yini.append(cc)
                            # definindo mes inicial
                            result = re.search('mes-inicio="(.*)" nome-curso=',
                                               aten)
                            cc = fun_result(result)
                            ls_mini.append(cc)
                            # definindo o ano final
                            result = re.search('ano-fim="(.*)" ano-inicio',
                                               aten)
                            cc = fun_result(result)
                            if result is None:
                                cc = 'VAZIO'
                            else:
                                cc = result.group(1)
                            if cc == '':
                                cc = 'ATUAL'
                            # definindo o mes final
                            result = re.search('mes-fim="(.*)" mes-inicio',
                                               aten)
                            cc = fun_result(result)
                            ls_yfin.append(cc)
                            if result is None:
                                cc = 'VAZIO'
                            else:
                                cc = result.group(1)
                            if cc == '':
                                cc = 'ATUAL'
                            ls_mfin.append(cc)
                            # definindo o curso
                            result = re.search(
                                'nome-curso=\"(.*)\" nome-curso-i',
                                aten)
                            cc = fun_result(result)
                            ls_curs.append(cc)
                            # definindo o tipo
                            result = re.search('tipo-ensino=\"(.*)\"\>\<',
                                               aten)
                            cc = fun_result(result)
                            ls_tipo.append(cc)
                            # definindo disciplinas
                            ensdisc = ens[k].find_all('disciplina')
                            if len(ensdisc) == 0:
                                print('nao ha discip nesta ativ ensino ', zipname)
                            else:
                                ls_dis = []
                                for kk in range(len(ensdisc)):
                                    dis = str(ensdisc[kk])
                                    result = re.search(
                                        '=\"\d\"\>(.*)\<\/disciplina', dis)
                                    cc = fun_result(result)
                                    ls_dis.append(cc)
                            ls_disc.append(ls_dis)
                            # ------------------------------------------------------------
        # DataFrame para os dados
        df_ens = pd.DataFrame({'INSTITUTION': ls_inst,
                               'YEAR_INI':  ls_yini,
                               'YEAR_FIN':  ls_yfin,
                               'MONTH_INI': ls_mfin,
                               'MONTH_FIN': ls_mfin,
                               'COURSE':    ls_curs,
                               'TYPE':      ls_tipo,
                               'DISC': ls_disc
                               })
        df_ens.sort_values(['YEAR_INI'], axis=0, inplace=True)
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_ensdisc.csv')
        df_ens.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(df_ens['YEAR_FIN']), ' atividades de ensino')
