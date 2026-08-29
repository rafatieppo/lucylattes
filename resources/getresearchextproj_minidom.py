"""Get research and extension projects from xml file."""

from resources.support_functions import list_append_proj_r_ext
import numpy as np
import pandas as pd


def getresearchextproj(zipname, minidomdoc):
    """Get research and extension projects from xml file."""
    # elem_curric_vitae = minidomdoc.getElementsByTagName('CURRICULO-VITAE')
    id_lattes = str(zipname.split('.')[0])
    chd_atuacprofs = minidomdoc.getElementsByTagName('ATUACOES-PROFISSIONAIS')
    if chd_atuacprofs.length > 0:
        len_chd_atuacprofs = len(chd_atuacprofs[0].childNodes)
    # child autuacoes profissionais -> atividades-de-participacao-em-projeto
        ls_enterprise = []
        ls_enterprise_code = []
        ls_proj = []
        ls_proj_seq = []
        ls_year_ini = []
        ls_year_end = []
        ls_situation = []
        ls_nature = []
        ls_description = []
        ls_members_name = []
        ls_members_id = []
        ls_member_coord = []
        ls_support = []
        for idx in range(len_chd_atuacprofs):
            enterprise = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('NOME-INSTITUICAO').nodeValue
            enterprise_code = chd_atuacprofs[0].childNodes[idx] \
                .getAttributeNode('CODIGO-INSTITUICAO').nodeValue
            # child atuacoes-profs -> ativ-de-partic-em-projeto ->partic-proj
            chd_part_proj = chd_atuacprofs[0].childNodes[idx] \
                .getElementsByTagName('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')
            if chd_part_proj.length == 0:
                ls_proj.append('VAZIO')
                ls_proj_seq.append('VAZIO')
                ls_year_ini.append('VAZIO')
                ls_year_end.append('VAZIO')
                ls_situation.append('VAZIO')
                ls_nature.append('VAZIO')
                ls_description.append('VAZIO')
                ls_members_name.append('VAZIO')
                ls_members_id.append('VAZIO')
                ls_member_coord.append('VAZIO')
                ls_support.append('VAZIO')
                ls_enterprise.append(enterprise)
                ls_enterprise_code.append(enterprise_code)
                # print(enterprise, ' has NO atividades-de-participac-em-proj')
            else:
                chd_part_proj = chd_atuacprofs[0].childNodes[idx] \
                    .getElementsByTagName('ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO')[0] \
                    .getElementsByTagName('PARTICIPACAO-EM-PROJETO')
                len_chd_part_proj = chd_part_proj.length
                for idy in range(len_chd_part_proj):
                    list_append_proj_r_ext(
                        chd_part_proj, idy, ls_proj, ls_proj_seq,
                        ls_year_ini, ls_year_end, ls_situation,
                        ls_nature, ls_description, ls_enterprise,
                        ls_enterprise_code, enterprise, enterprise_code,
                        ls_members_name, ls_members_id, ls_member_coord,
                        ls_support)
        df_ppe = pd.DataFrame({'ID': np.repeat(id_lattes, len(ls_proj)),
                               'TITLE': ls_proj,
                               'SEQ_PROJ': ls_proj_seq,
                               'YEAR': ls_year_ini,
                               'YEAR_FIN': ls_year_end,
                               'SITUATION': ls_situation,
                               'NATURE': ls_nature,
                               'DESCRIPTION': ls_description,
                               'MEMBERS': ls_members_name,
                               'COORDENA': ls_member_coord,
                               'SUPPORT': ls_support,
                               'ADDRESS_PPE_ENTERP': ls_enterprise,
                               'ADDRESS_PPE_ENTERP_CODE': ls_enterprise_code})
        pathfilename = str('./csv_producao/' + id_lattes + '_ppe.csv')
        df_ppe.to_csv(pathfilename, index=False)
        print('The file ', pathfilename, ' has been writed.')
        # return df_ppe
    else:
        print('The id Lattes ', id_lattes, ' has NO ATUACOES-PROFISSIONAIS.')
