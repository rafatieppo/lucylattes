"""Get dados-gerais from xml file."""

import pandas as pd


def getgeneraldata(zipname, minidomdoc):
    """Get dados-gerais from minidom."""
    id_lattes = str(zipname.split('.')[0])
    elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    last_update = elem_curric_vitae[0].getAttributeNode(
        'DATA-ATUALIZACAO').nodeValue
    if len(last_update) == 8:
        last_update = last_update[0:2] + '-' + \
            last_update[2:4] + '-' + last_update[4:8]
    if elem_curric_vitae[0].hasChildNodes is not True:
        # curriculo-vitae -> child dgerais
        chd_dgerais = minidomdoc.getElementsByTagName('DADOS-GERAIS')
        chd_dgerais_len = len(chd_dgerais[0].childNodes)
        print('DADOS-GERAIS has ', chd_dgerais_len, ' childs')
        full_name = chd_dgerais[0].getAttributeNode(
            'NOME-COMPLETO').nodeValue
        last_name = full_name.split(' ')[-1]
        citation_names = chd_dgerais[0].getAttributeNode(
            'NOME-EM-CITACOES-BIBLIOGRAFICAS').nodeValue
        birth_city = chd_dgerais[0].getAttributeNode(
            'CIDADE-NASCIMENTO').nodeValue
        if birth_city == '':
            birth_city = 'VAZIO'
        birth_state = chd_dgerais[0].getAttributeNode(
            'UF-NASCIMENTO').nodeValue
        if birth_state == '':
            birth_state = 'VAZIO'
        if chd_dgerais[0].getAttributeNode('ORCID-ID') is None:
            orcid = 'VAZIO'
        else:
            orcid = chd_dgerais[0].getAttributeNode('ORCID-ID').nodeValue
        # child dgerais -> child resumocv
        chd_dgerais_chd_resumocv = chd_dgerais[0].getElementsByTagName(
            'RESUMO-CV')
        if chd_dgerais_chd_resumocv.length >= 1:
            cv_abstract = chd_dgerais_chd_resumocv[0].getAttributeNode(
                'TEXTO-RESUMO-CV-RH').value
        else:
            cv_abstract = 'VAZIO'
        # child dgerais -> child endereco
        chd_dgerais_chd_endereco = chd_dgerais[0].getElementsByTagName(
            'ENDERECO')
        # child dgerais -> child endereco -> child endereco profissional
        chd_dgerais_chd_endereco_chd_endprof = chd_dgerais_chd_endereco[0] \
            .getElementsByTagName('ENDERECO-PROFISSIONAL')
        if chd_dgerais_chd_endereco_chd_endprof.length == 0:
            enterprise = 'Vazio'
            enterprise_code = 'Vazio'
        else:
            enterprise = chd_dgerais_chd_endereco_chd_endprof[0].getAttributeNode(
                'NOME-INSTITUICAO-EMPRESA').value
            enterprise_code = chd_dgerais_chd_endereco_chd_endprof[0] \
                .getAttributeNode('CODIGO-INSTITUICAO-EMPRESA').value
        # child dgerais -> child formacao academ -> child doutorado
        # chd_dgerais_chd_formacao = chd_dgerais[0].getElementsByTagName(
        #     'FORMACAO-ACADEMICA-TITULACAO')
        # chd_dgerais_chd_formacao_chd_doc = chd_dgerais_chd_formacao[0] \
        #     .getElementsByTagName('DOUTORADO')
        # dout_inst = chd_dgerais_chd_formacao_chd_doc[0].getAttributeNode(
        #     'NOME-INSTITUICAO').value
        # dout_curs = chd_dgerais_chd_formacao_chd_doc[0].getAttributeNode(
        #     'NOME-CURSO').value
        # dout_yini = chd_dgerais_chd_formacao_chd_doc[0].getAttributeNode(
        #     'ANO-DE-INICIO').value
        # dout_yfin = chd_dgerais_chd_formacao_chd_doc[0].getAttributeNode(
        #     'ANO-DE-CONCLUSAO').value
        # output
        df_fullname = pd.DataFrame({'ID': pd.Series(id_lattes),
                                    'FULL_NAME': pd.Series(full_name),
                                    'LAST_NAME': pd.Series(last_name),
                                    'CITADO': pd.Series(citation_names),
                                    'CITY': pd.Series(birth_city),
                                    'STATE': pd.Series(birth_state),
                                    'RESUME': pd.Series(cv_abstract),
                                    'UPDATE': pd.Series(last_update),
                                    'ADDRESS_ENTERP': pd.Series(enterprise),
                                    'ORCID': pd.Series(orcid),
                                    'ADDRESS_ENTERP_CODE': pd.Series(enterprise_code),
                                    # 'DOC_INST': pd.Series(dout_inst),
                                    # 'DOC_COURSE': pd.Series(dout_curs),
                                    # 'DOC_YEAR_INI': pd.Series(dout_yini),
                                    # 'DOC_YEAR_FIN': pd.Series(dout_yfin)
                                    })

        pathfilename = str('./csv_producao/' + id_lattes + '_fullname.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_fullname
