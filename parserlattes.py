# ------------------------------------------------------------
# projetos de pesquisa institucionalizados / FAP
# ------------------------------------------------------------

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile


def getprojpesqext(zipname):
    # lendo do zipfile
    archive = zipfile.ZipFile(str(zipname), 'r')
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
    latid = zipname.split('.')[0]
    pathfilename = str('./csv_ppe/' + latid + '_ppe'  '.csv')
    df_ppe.to_csv(pathfilename, index=False)


# ------------------------------------------------------------
# iniciando funcao para producao tecnica do pesquisador - cursos etc
# ------------------------------------------------------------
