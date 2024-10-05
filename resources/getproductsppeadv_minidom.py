"""Get products adivising of projects from xml file."""

import numpy as np
import pandas as pd


def getproductsppeadv(zipname, minidomdoc):
    """Get products adivising of projects from xml file."""
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
        ls_seq_adv = []
        ls_titl_adv = []
        ls_type_adv = []
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
                            chd_prods_adv = chd_proj_pesq[idz] \
                                .getElementsByTagName('ORIENTACOES')
                            len_chd_prods_adv = chd_prods_adv.length
                            if len_chd_prods_adv >= 1:
                                for idw in range(len_chd_prods_adv):
                                    chd_prod_adv = chd_prods_adv[idw] \
                                        .getElementsByTagName('ORIENTACAO')
                                    seq_adv = chd_prod_adv[0] \
                                        .getAttributeNode('SEQUENCIA-ORIENTACAO').nodeValue
                                    titl_adv = chd_prod_adv[0] \
                                        .getAttributeNode('TITULO-ORIENTACAO').nodeValue
                                    type_adv = chd_prod_adv[0] \
                                        .getAttributeNode('TIPO-ORIENTACAO').nodeValue
                                    ls_idlattes.append(id_lattes)
                                    ls_enterprise.append(enterprise)
                                    ls_enterprise_code.append(enterprise_code)
                                    ls_proj.append(proj)
                                    ls_seq_proj.append(seq_proj)
                                    ls_year_ini.append(year_ini)
                                    ls_year_end.append(year_end)
                                    ls_seq_adv.append(seq_adv)
                                    ls_titl_adv.append(titl_adv)
                                    ls_type_adv.append(type_adv)

    if len(ls_idlattes) >= 1:
        df_prods_ct_proj = pd.DataFrame({
            'ID': ls_idlattes,
            'ADDRESS_PPE_ENTERP': ls_enterprise,
            'ADDRESS_PPE_ENTERP_CODE': ls_enterprise_code,
            'TITLE_PROJ': ls_proj,
            'SEQ_PROJ': ls_seq_proj,
            'YEAR': ls_year_ini,
            'YEAR_FIN': ls_year_end,
            'SEQ_ADV': ls_seq_adv,
            'TITLE_ADV': ls_titl_adv,
            'TYPE_ADV': ls_type_adv})
        pathfilename = str('./csv_producao/' + id_lattes + '_ppe_prods_adv.csv')
        df_prods_ct_proj.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
    # return df_ppe
    else:
        print('The id Lattes ', id_lattes, ' has NO PRODUCOES-CT-DO-PROJETO.')
