"""Get formacao academica -> doutorado from xml file."""

import numpy as np
import pandas as pd


def getgeneraldata_dout(zipname, minidomdoc):
    """Get dados-gerais doutorado from minidom."""
    id_lattes = str(zipname.split('.')[0])
    elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    if elem_curric_vitae[0].hasChildNodes is not True:
        # curriculo-vitae -> child dgerais
        chd_dgerais = minidomdoc.getElementsByTagName('DADOS-GERAIS')
        chd_dgerais_len = len(chd_dgerais[0].childNodes)
        print('DADOS-GERAIS has ', chd_dgerais_len, ' childs')
        # child dgerais -> child formacao academ -> child doutorado
        lsinst, lscourse, lscour_yini, lscour_yfin = [], [], [], []
        chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
            'FORMACAO-ACADEMICA-TITULACAO')
        chd_dgerais_chd_formacao_chd_dout = chd_dgerais_chd_formacao[0] \
            .getElementsByTagName('DOUTORADO')
        if len(chd_dgerais_chd_formacao_chd_dout) > 0:
            for idx in range(len(chd_dgerais_chd_formacao_chd_dout)):
                instit = chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                    'NOME-INSTITUICAO').value
                if instit is None:
                    lsinst.append('VAZIO')
                else:
                    lsinst.append(instit)
                course = chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'NOME-CURSO').value
                if course == '':
                    lscourse.append('VAZIO')
                else:
                    lscourse.append(course)
                course_yini = chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'ANO-DE-INICIO').value
                if course_yini == '':
                    lscour_yini.append(0)
                else:
                    lscour_yini.append(course_yini)
                course_yfin = chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
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
                                    'DOUT_INST': lsinst,
                                    'DOUT_COURSE': lscourse,
                                    'DOUT_YEAR_INI': lscour_yini,
                                    'DOUT_YEAR_FIN': lscour_yfin,
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_form_dout.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
