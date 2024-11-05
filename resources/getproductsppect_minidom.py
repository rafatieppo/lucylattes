"""Get products ct of projects from xml file."""

import numpy as np
import pandas as pd


def getproductsppect(zipname, minidomdoc):
    """Get products ct of projects from xml file."""
    # elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    id_lattes = str(zipname.split('.')[0])
    chd_atuacprofs = minidomdoc.getElementsByTagName('ATUACOES-PROFISSIONAIS')
    if chd_atuacprofs.length > 0:
        len_chd_atuacprofs = len(chd_atuacprofs[0].childNodes)
    # child autuacoes profissionais -> atividades-de-participacao-em-projeto
        ls_idlattes = []
        ls_enterprise = []
        ls_enterprise_code = []
        ls_proj = []
        ls_seq_proj = []
        ls_year_ini = []
        ls_year_end = []
        ls_nature = []
        ls_seq_prod = []
        ls_titl_prod = []
        ls_type_prod = []
        for idx in range(len_chd_atuacprofs):
            enterprise = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('NOME-INSTITUICAO').nodeValue
            enterprise_code = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('CODIGO-INSTITUICAO').nodeValue
            # child atuacoes-profs -> ativ-de-partic-em-projeto ->partic-proj
            chd_part_ativ_part_proj = chd_atuacprofs[0].childNodes[idx] \
                .getElementsByTagName('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')
            if chd_part_ativ_part_proj.length == 0:
                pass
                # print(enterprise, ' has NO atividades-de-participac-em-proj')
            else:
                chd_part_proj = chd_atuacprofs[0].childNodes[idx] \
                    .getElementsByTagName('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')[0] \
                    .getElementsByTagName('PARTICIPACAO-EM-PROJETO')
                len_chd_part_proj = chd_part_proj.length
                for idy in range(len_chd_part_proj):
                    chd_proj_pesq = chd_part_proj[idy] \
                        .getElementsByTagName('PROJETO-DE-PESQUISA')
                    len_chd_proj_pesq = chd_proj_pesq.length
                    if len_chd_proj_pesq >= 1:
                        for idz in range(len_chd_proj_pesq):
                            proj = chd_proj_pesq[idz] \
                                .getAttributeNode('NOME-DO-PROJETO').nodeValue
                            seq_proj = chd_proj_pesq[idz] \
                                .getAttributeNode('SEQUENCIA-PROJETO').nodeValue
                            year_ini = chd_proj_pesq[idz] \
                                .getAttributeNode('ANO-INICIO').nodeValue
                            if year_ini == '':
                                year_ini = 'VAZIO'
                            year_end = chd_proj_pesq[idz] \
                                .getAttributeNode('ANO-FIM').nodeValue
                            if year_end == '':
                                year_end = 'ATUAL'
                            chd_prods_proj = chd_proj_pesq[idz] \
                                .getElementsByTagName('PRODUCOES-CT-DO-PROJETO')
                            len_chd_prods_proj = chd_prods_proj.length
                            if len_chd_prods_proj >= 1:
                                for idw in range(len_chd_prods_proj):
                                    chd_prod_proj = chd_prods_proj[idw] \
                                        .getElementsByTagName('PRODUCAO-CT-DO-PROJETO')
                                    seq_prod = chd_prod_proj[0] \
                                        .getAttributeNode('SEQUENCIA-PRODUCAO-CT').nodeValue
                                    titl_prod = chd_prod_proj[0] \
                                        .getAttributeNode('TITULO-DA-PRODUCAO-CT').nodeValue
                                    type_prod = chd_prod_proj[0] \
                                        .getAttributeNode('TIPO-PRODUCAO-CT').nodeValue
                                    ls_idlattes.append(id_lattes)
                                    ls_enterprise.append(enterprise)
                                    ls_enterprise_code.append(enterprise_code)
                                    ls_proj.append(proj)
                                    ls_seq_proj.append(seq_proj)
                                    ls_year_ini.append(year_ini)
                                    ls_year_end.append(year_end)
                                    ls_seq_prod.append(seq_prod)
                                    ls_titl_prod.append(titl_prod)
                                    ls_type_prod.append(type_prod)

    if len(ls_idlattes) >= 1:
        df_prods_ct_proj = pd.DataFrame({
            'ID': ls_idlattes,
            'ADDRESS_PPE_ENTERP': ls_enterprise,
            'ADDRESS_PPE_ENTERP_CODE': ls_enterprise_code,
            'TITLE_PROJ': ls_proj,
            'SEQ_PROJ': ls_seq_proj,
            'YEAR': ls_year_ini,
            'YEAR_FIN': ls_year_end,
            'SEQ_PROD': ls_seq_prod,
            'TITLE_PROD': ls_titl_prod,
            'TYPE_PROD': ls_type_prod})
        pathfilename = str('./csv_producao/' + id_lattes + '_ppe_prods_ct.csv')
        df_prods_ct_proj.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
    # return df_ppe
    else:
        print('The id Lattes ', id_lattes, ' has NO PRODUCOES-CT-DO-PROJETO.')
