"""Get formacao academica -> mestrado from xml file."""

import numpy as np
import pandas as pd


def getgeneraldata_mest(zipname, minidomdoc):
    """Get dados-gerais mestrado from minidom."""
    id_lattes = str(zipname.split('.')[0])
    elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    if elem_curric_vitae[0].hasChildNodes is not True:
        # curriculo-vitae -> child dgerais
        chd_dgerais = minidomdoc.getElementsByTagName('DADOS-GERAIS')
        chd_dgerais_len = len(chd_dgerais[0].childNodes)
        print('DADOS-GERAIS has ', chd_dgerais_len, ' childs')
        # child dgerais -> child formacao academ -> child mestrado
        mest_inst, mest_curs, mest_yini, mest_yfin = [], [], [], []
        chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
            'FORMACAO-ACADEMICA-TITULACAO')
        chd_dgerais_chd_formacao_chd_mest = chd_dgerais_chd_formacao[0] \
            .getElementsByTagName('MESTRADO')
        if len(chd_dgerais_chd_formacao_chd_mest) > 0:
            for idx in range(len(chd_dgerais_chd_formacao_chd_mest)):
                mest_inst.append(
                    chd_dgerais_chd_formacao_chd_mest[0].getAttributeNode(
                        'NOME-INSTITUICAO').value)
                mest_curs.append(
                    chd_dgerais_chd_formacao_chd_mest[0].getAttributeNode(
                        'NOME-CURSO').value)
                mest_yini.append(
                    chd_dgerais_chd_formacao_chd_mest[0].getAttributeNode(
                        'ANO-DE-INICIO').value)
                mest_yfin.append(
                    chd_dgerais_chd_formacao_chd_mest[0].getAttributeNode(
                        'ANO-DE-CONCLUSAO').value)
        # output
        df_fullname = pd.DataFrame({'ID': list(
            np.repeat(id_lattes, len(chd_dgerais_chd_formacao_chd_mest))),
                                    'MEST_INST': mest_inst,
                                    'MEST_COURSE': mest_curs,
                                    'MEST_YEAR_INI': mest_yini,
                                    'MEST_YEAR_FIN': mest_yfin,
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_form_mest.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
