"""Get teaching from xml file."""

import numpy as np
import pandas as pd


def getteaching(zipname, minidomdoc):
    """Get teaching from xml file."""
    # elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    id_lattes = str(zipname.split('.')[0])
    # child autuacoes profissionais
    chd_atuacprofs = minidomdoc.getElementsByTagName('ATUACOES-PROFISSIONAIS')
    if chd_atuacprofs.length > 0:
        len_chd_atuacprofs = len(chd_atuacprofs[0].childNodes)
        ls_enterprise = []
        ls_enterprise_code = []
        ls_type = []
        ls_year_ini = []
        ls_year_fin = []
        ls_month_ini = []
        ls_month_fin = []
        ls_degree = []
        ls_degree_id = []
        ls_courses = []
        for idx in range(len_chd_atuacprofs):
            enterprise = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('NOME-INSTITUICAO').nodeValue
            enterprise_code = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('CODIGO-INSTITUICAO').nodeValue

            # child atuacoes-profs -> atividades-de-ensino
            chd_ativs_ensi = chd_atuacprofs[0].childNodes[idx] \
                .getElementsByTagName('ATIVIDADES-DE-ENSINO')
            if chd_ativs_ensi.length == 0:
                ls_enterprise.append(enterprise)
                ls_enterprise_code.append(enterprise_code)
                ls_type.append('VAZIO')
                ls_year_ini.append('VAZIO')
                ls_year_fin.append('VAZIO')
                ls_month_ini.append('VAZIO')
                ls_month_fin.append('VAZIO')
                ls_degree.append('VAZIO')
                ls_degree_id.append('VAZIO')
                ls_courses.append('VAZIO')
                # print(enterprise, ' has NO atividades-de-ensino')

            else:
                # child atuacoes-profs -> atividades-de-ensino -> ensino
                chd_ensino = chd_ativs_ensi[0] \
                    .getElementsByTagName('ENSINO')
                for idy in range(chd_ensino.length):
                    typee = chd_ensino[idy].getAttributeNode(
                        'TIPO-ENSINO').nodeValue
                    year_ini = chd_ensino[idy].getAttributeNode(
                        'ANO-INICIO').nodeValue
                    year_fin = chd_ensino[idy].getAttributeNode(
                        'ANO-FIM').nodeValue
                    if year_fin == '':
                        year_fin = 'ATUAL'
                    month_ini = chd_ensino[idy].getAttributeNode(
                        'MES-INICIO').nodeValue
                    month_fin = chd_ensino[idy].getAttributeNode(
                        'MES-FIM').nodeValue
                    degree = chd_ensino[idy].getAttributeNode(
                        'NOME-CURSO').nodeValue
                    degree_id = chd_ensino[idy].getAttributeNode(
                        'CODIGO-CURSO').nodeValue

                    # child atuacoes-profs -> atvs-d-ensin -> ensino -> discips
                    chd_discip = chd_ensino[idy] \
                        .getElementsByTagName('DISCIPLINA')
                    ls_courses_temp = []
                    for idw in range(chd_discip.length):
                        cour = chd_discip[idw].childNodes
                        cour_value = cour[0].nodeValue
                        ls_courses_temp.append(cour_value)

                    # append into main lists
                    ls_enterprise.append(enterprise)
                    ls_enterprise_code.append(enterprise_code)
                    ls_type.append(typee)
                    ls_year_ini.append(year_ini)
                    ls_year_fin.append(year_fin)
                    ls_month_ini.append(month_ini)
                    ls_month_fin.append(month_fin)
                    ls_degree.append(degree)
                    ls_degree_id.append(degree_id)
                    ls_courses.append(ls_courses_temp)

        df_teaching = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                    len(ls_enterprise)),
                                    'INSTITUTION': ls_enterprise,
                                    'INSTITUTION_CODE': ls_enterprise_code,
                                    'YEAR':  ls_year_ini,
                                    'YEAR_FIN':  ls_year_fin,
                                    'MONTH_INI': ls_month_ini,
                                    'MONTH_FIN': ls_month_fin,
                                    'DEGREE': ls_degree,
                                    'DEGREE_ID': ls_degree_id,
                                    'TYPE': ls_type,
                                    'TITLE': ls_courses})
        pathfilename = str('./csv_producao/' + id_lattes + '_teaching.csv')
        df_teaching.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')

    else:
        print('The id Lattes ', id_lattes, ' has NO ATUACOES-PROFISSIONAIS.')
