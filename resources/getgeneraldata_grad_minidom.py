"""Get formacao academica -> graduacao from xml file."""

import numpy as np
import pandas as pd


def getgeneraldata_grad(zipname, minidomdoc):
    """Get dados-gerais graduacao from minidom."""
    id_lattes = str(zipname.split('.')[0])
    elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    if elem_curric_vitae[0].hasChildNodes is not True:
        # curriculo-vitae -> child dgerais
        chd_dgerais = minidomdoc.getElementsByTagName('DADOS-GERAIS')
        chd_dgerais_len = len(chd_dgerais[0].childNodes)
        print('DADOS-GERAIS has ', chd_dgerais_len, ' childs')
        # child dgerais -> child formacao academ -> child graduacao
        lsinst, lscourse, lscour_yini, lscour_yfin = [], [], [], []
        chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
            'FORMACAO-ACADEMICA-TITULACAO')
        chd_dgerais_chd_formacao_chd_grad = chd_dgerais_chd_formacao[0] \
            .getElementsByTagName('GRADUACAO')
        if len(chd_dgerais_chd_formacao_chd_grad) > 0:
            for idx in range(len(chd_dgerais_chd_formacao_chd_grad)):
                instit = chd_dgerais_chd_formacao_chd_grad[0].getAttributeNode(
                    'NOME-INSTITUICAO').value
                if instit == '':
                    lsinst.append('VAZIO')
                else:
                    lsinst.append(instit)
                course = chd_dgerais_chd_formacao_chd_grad[0].getAttributeNode(
                        'NOME-CURSO').value
                if course == '':
                    lscourse.append('VAZIO')
                else:
                    lscourse.append(course)
                course_yini = chd_dgerais_chd_formacao_chd_grad[0].getAttributeNode(
                        'ANO-DE-INICIO').value
                if course_yini == '':
                    lscour_yini.append(0)
                else:
                    lscour_yini.append(course_yini)
                course_yfin = chd_dgerais_chd_formacao_chd_grad[0].getAttributeNode(
                        'ANO-DE-CONCLUSAO').value
                if course_yfin == '':
                    lscour_yfin.append(0)
                else:
                    lscour_yfin.append(course_yfin)
        else:
            lsinst.append('VAZIO')
            lscourse.append('VAZIO')
            lscour_yini.append(0)
            lscour_yfin.append(0)
        # output
        df_fullname = pd.DataFrame({'ID': list(
            np.repeat(id_lattes, len(lsinst))),
                                    'LSINT': lsinst,
                                    'GRAD_COURSE': lscourse,
                                    'GRAD_YEAR_INI': lscour_yini,
                                    'GRAD_YEAR_FIN': lscour_yfin,
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_form_grad.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
