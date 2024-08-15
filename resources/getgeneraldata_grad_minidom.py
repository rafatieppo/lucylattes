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
        grad_inst, grad_curs, grad_yini, grad_yfin = [], [], [], []
        chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
            'FORMACAO-ACADEMICA-TITULACAO')
        chd_dgerais_chd_formacao_chd_grad = chd_dgerais_chd_formacao[0] \
            .getElementsByTagName('GRADUACAO')
        if len(chd_dgerais_chd_formacao_chd_grad) > 0:
            for idx in range(len(chd_dgerais_chd_formacao_chd_grad)):
                grad_inst.append(
                    chd_dgerais_chd_formacao_chd_grad[idx].getAttributeNode(
                        'NOME-INSTITUICAO').value)
                grad_curs.append(
                    chd_dgerais_chd_formacao_chd_grad[idx].getAttributeNode(
                        'NOME-CURSO').value)
                grad_yini.append(
                    chd_dgerais_chd_formacao_chd_grad[idx].getAttributeNode(
                        'ANO-DE-INICIO').value)
                grad_yfin.append(
                    chd_dgerais_chd_formacao_chd_grad[idx].getAttributeNode(
                        'ANO-DE-CONCLUSAO').value)
        # output
        df_fullname = pd.DataFrame({'ID': list(
            np.repeat(id_lattes, len(chd_dgerais_chd_formacao_chd_grad))),
                                    'GRAD_INST': grad_inst,
                                    'GRAD_COURSE': grad_curs,
                                    'GRAD_YEAR_INI': grad_yini,
                                    'GRAD_YEAR_FIN': grad_yfin,
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_form_grad.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
