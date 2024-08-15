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
        dout_inst, dout_curs, dout_yini, dout_yfin = [], [], [], []
        chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
            'FORMACAO-ACADEMICA-TITULACAO')
        chd_dgerais_chd_formacao_chd_dout = chd_dgerais_chd_formacao[0] \
            .getElementsByTagName('DOUTORADO')
        if len(chd_dgerais_chd_formacao_chd_dout) > 0:
            for idx in range(len(chd_dgerais_chd_formacao_chd_dout)):
                dout_inst.append(
                    chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'NOME-INSTITUICAO').value)
                dout_curs.append(
                    chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'NOME-CURSO').value)
                dout_yini.append(
                    chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'ANO-DE-INICIO').value)
                dout_yfin.append(
                    chd_dgerais_chd_formacao_chd_dout[0].getAttributeNode(
                        'ANO-DE-CONCLUSAO').value)
        # output
        df_fullname = pd.DataFrame({'ID': list(
            np.repeat(id_lattes, len(chd_dgerais_chd_formacao_chd_dout))),
                                    'DOUT_INST': dout_inst,
                                    'DOUT_COURSE': dout_curs,
                                    'DOUT_YEAR_INI': dout_yini,
                                    'DOUT_YEAR_FIN': dout_yfin,
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_form_dout.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
