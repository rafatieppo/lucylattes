"""Several functions for support another function."""

from tabulate import tabulate
import numpy as np
import pandas as pd


def list_append_proj_r_ext(chd_part_proj, idy,
                           ls_proj, ls_year_ini, ls_year_end,
                           ls_nature, ls_enterprise, ls_enterprise_code,
                           enterprise, enterprise_code,
                           ls_members_name, ls_members_id, ls_member_coord):
    """Append lists with data from each research extension project w member."""
    ppe = chd_part_proj[idy] \
        .getElementsByTagName('PROJETO-DE-PESQUISA')
    len_ppe = ppe.length
    # ---------------------------------
    # -----------------------------------
    if len_ppe <= 0:
        proj = 'VAZIO'
        year_ini = 'VAZIO'
        year_ini = 'VAZIO'
        year_end = 'VAZIO'
        nature = 'VAZIO'
        ls_proj.append(proj)
        ls_year_ini.append(year_ini)
        ls_year_end.append(year_end)
        ls_nature.append(nature)
        ls_enterprise.append(enterprise)
        ls_enterprise_code.append(enterprise_code)
        nn = 'VAZIO'
        nn_id = 'VAZIO'
        nn_coord = 'VAZIO'
        ls_members_name.append(nn)
        ls_members_id.append(nn_id)
        ls_member_coord.append(nn_coord)

    elif len_ppe == 1:
        proj = ppe[0] \
            .getAttributeNode('NOME-DO-PROJETO').nodeValue
        year_ini = ppe[0] \
            .getAttributeNode('ANO-INICIO').nodeValue
        if year_ini == '':
            year_ini = 'VAZIO'
        year_end = ppe[0] \
            .getAttributeNode('ANO-FIM').nodeValue
        if year_end == '':
            year_end = 'ATUAL'
        nature = ppe[0] \
            .getAttributeNode('NATUREZA').nodeValue
        ls_proj.append(proj)
        ls_year_ini.append(year_ini)
        ls_year_end.append(year_end)
        ls_nature.append(nature)
        ls_enterprise.append(enterprise)
        ls_enterprise_code.append(enterprise_code)
        # child atacoes profs->ativ-de-partic-proj->proj-pesq->eqip
        team = ppe[0].getElementsByTagName('EQUIPE-DO-PROJETO')
        len_chd_members = team[0].childNodes.length
        if len_chd_members >= 1:
            nn = []
            nn_id = []
            nn_coord = []
            for idw in range(len_chd_members):
                list_append_proj_members(
                    team, idw, nn, nn_id, nn_coord)
            ls_members_name.append(nn)
            ls_members_id.append(nn_id)
            ls_member_coord.append(nn_coord)

    # ---------------------------------
    # --------------------------------
    # if there are 2 or more projects in the same year
    elif len_ppe > 1:
        for idv in range(len_ppe):
            # print(idv, '---idv')
            proj = ppe[idv] \
                .getAttributeNode('NOME-DO-PROJETO').nodeValue
            # print(proj)
            year_ini = ppe[idv] \
                .getAttributeNode('ANO-INICIO').nodeValue
            if year_ini == '':
                year_ini = 'VAZIO'
            year_end = ppe[idv] \
                .getAttributeNode('ANO-FIM').nodeValue
            if year_end == '':
                year_end = 'ATUAL'
            nature = ppe[idv] \
                .getAttributeNode('NATUREZA').nodeValue
            ls_proj.append(proj)
            ls_year_ini.append(year_ini)
            ls_year_end.append(year_end)
            ls_nature.append(nature)
            ls_enterprise.append(enterprise)
            ls_enterprise_code.append(enterprise_code)
            # child atuacao-prof->ativ-de-partic-proj->proj-pesq->eqip
            team = ppe[idv].getElementsByTagName('EQUIPE-DO-PROJETO')
            len_chd_members = team[0].childNodes.length
            if len_chd_members >= 1:
                nn = []
                nn_id = []
                nn_coord = []
                for idw in range(len_chd_members):
                    list_append_proj_members(
                        team, idw, nn, nn_id, nn_coord)
                ls_members_name.append(nn)
                ls_members_id.append(nn_id)
                ls_member_coord.append(nn_coord)
            # return ppe
    # else:
    #     proj = ppe[0] \
    #         .getAttributeNode('NOME-DO-PROJETO').nodeValue
    #     year_ini = ppe[0] \
    #         .getAttributeNode('ANO-INICIO').nodeValue
    #     if year_ini == '':
    #         year_ini = 'VAZIO'
    #     year_end = ppe[0] \
    #         .getAttributeNode('ANO-FIM').nodeValue
    #     if year_end == '':
    #         year_end = 'ATUAL'
    #     nature = ppe[0] \
    #         .getAttributeNode('NATUREZA').nodeValue
    #     ls_proj.append(proj)
    #     ls_year_ini.append(year_ini)
    #     ls_year_end.append(year_end)
    #     ls_nature.append(nature)
    #     ls_enterprise.append(enterprise)
    #     ls_enterprise_code.append(enterprise_code)
    #     # child atacoes profs->ativ-de-partic-proj->proj-pesq->eqip
    #     team = ppe[0].getElementsByTagName('EQUIPE-DO-PROJETO')
    #     len_chd_members = team[0].childNodes.length
    #     if len_chd_members >= 1:
    #         nn = []
    #         nn_id = []
    #         nn_coord = []
    #         for idw in range(len_chd_members):
    #             list_append_proj_members(
    #                 team, idw, nn, nn_id, nn_coord)
    #         ls_members_name.append(nn)
    #         ls_members_id.append(nn_id)
    #         ls_member_coord.append(nn_coord)
    #     # return ppe


def list_append_proj_members(team, idw, nn, nn_id, nn_coord):
    """Append lists with data from members for each project."""
    name = team[0] \
        .getElementsByTagName('INTEGRANTES-DO-PROJETO')[idw] \
        .getAttributeNode('NOME-COMPLETO').nodeValue
    name_id = team[0] \
        .getElementsByTagName('INTEGRANTES-DO-PROJETO')[idw] \
        .getAttributeNode('NRO-ID-CNPQ').nodeValue
    coord = team[0] \
        .getElementsByTagName('INTEGRANTES-DO-PROJETO')[idw] \
        .getAttributeNode('FLAG-RESPONSAVEL').nodeValue
    nn.append(name)
    nn_id.append(name_id)
    nn_coord.append(coord)


def yearlimit_forfilter():
    """Return a list with initial and end year to filter data."""
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    yearini = config_file.readlines()[5].split(':')[1]
    yearini = yearini.rstrip('\n')
    yearini = yearini.strip(' ')
    yearini = int(yearini)
    config_file.close()
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    yearend = config_file.readlines()[6].split(':')[1]
    yearend = yearend.rstrip('\n')
    yearend = yearend.strip(' ')
    yearend = int(yearend)
    config_file.close()
    ls_year_iniend = [yearini, yearend]
    return ls_year_iniend


# def run_capes_index():
#     """Return 1 or 0 from config.txt to run or not capes index."""
#     config_file = open('./config.txt', 'r', encoding='utf-8')
#     run_indcapes = config_file.readlines()[7].split(':')[1]
#     config_file.close()
#     run_indcapes = run_indcapes.rstrip('\n')
#     run_indcapes = run_indcapes.strip(' ')
#     run_indcapes = int(run_indcapes)
#     return run_indcapes


def droprow_nullyear(df):
    """Drop row with null initial year or null year."""
    lsindex = []
    for idx in range(len(df['ID'])):
        yini = df['YEAR'].iloc[idx]
        try:
            int(yini)
            yini = int(yini)
        except ValueError:
            # if pd.isna(yini) or yini == 'VAZIO':
            print('------------------------------------------------------------\n' +
                  'ATTENTION \n' +
                  'Impossible to get INITIAL YEAR or YEAR for the title: \n' +
                  str(df['TITLE'].iloc[idx]) + ' \n from researcher: ' +
                  str(df['FULL_NAME'].iloc[idx]) + '... DROPPED title \n' +
                  str('Check the cv Lattes \n') +
                  '------------------------------------------------------------')
            lsindex.append(idx)
            print(idx)
        else:
            yini = int(float(yini))
    df.drop(lsindex, axis=0, inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


def writecsv_from_lspdseries(lspdseries, pathfilename, elsemsg):
    """Return a df and write a csv, both from lspdseries."""
    if len(lspdseries) >= 1:
        df = pd.DataFrame(i.values.transpose() for i in lspdseries)
        df.columns = lspdseries[0].index
        pathfilename = pathfilename
        df.to_csv(pathfilename, index=False, sep=',')
        print('The file ', pathfilename, ' has been writed.')
        return df
    else:
        print(elsemsg)


# def qualis_file():
#     """Read config file and return which qualis file was assigned."""
#     config_file = open('./config.txt', 'r')
#     # config_file = open('./config.txt', 'r', encoding='utf-8')
#     qf = config_file.readlines()[4].split(':')[1]
#     qf = qf.rstrip('\n')
#     qf = qf.strip(' ')
#     config_file.close()
#     return qf


def pg_name():
    """Read config file and return pg name."""
    config_file = open('./config_tk.txt', 'r')
    # config_file = open('./config.txt', 'r', encoding='utf-8')
    pgname = config_file.readlines()[3] # .split(':')[1]
    pgname = pgname.rstrip('\n')
    pgname = pgname.strip(' ')
    config_file.close()
    return pgname


def report_resch_teach(idlattes, rep_setup_file):
    """Return a table with teaching activties for a researcher."""
    if rep_setup_file['teaching']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_teaching_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        if len(df) >= 1:
            df.reset_index(inplace=True, drop=True)
            df = df.loc[:, ['INSTITUTION', 'YEAR', 'MONTH_INI', 'YEAR_FIN',
                            'MONTH_FIN', 'DEGREE', 'TYPE', 'TITLE']]
            df.columns = ['INSTITUTION', 'YI', 'MI', 'YI',
                          'MF', 'DEGREE', 'TYPE', 'TITLE']
            df.reset_index(inplace=True, drop=True)
            tablhtml = tabulate(df, headers='keys', tablefmt='html')
            return tablhtml
        else:
            return '<b>Não há disciplinas para o pesquisador.</b>'
    else:
        return '<b>Não há disciplinas para o pesquisador.</b>'


def report_resch_advi_done_each(idlattes, rep_setup_file):
    """Return table with all advising summary production for each researcher."""
    if rep_setup_file['advis_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advis_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        df = df.reset_index(drop=True)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        # replace categories names in nature column
        colname = 'NATURE'
        cond = [
            df[colname] == 'Dissertação de mestrado',
            df[colname] == 'Supervisão de pós-doutorado',
            df[colname] == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO',
            df[colname] == 'INICIACAO_CIENTIFICA',
            df[colname] == 'Tese de doutorado',
            df[colname] == 'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO',
            df[colname] == 'ORIENTACAO-DE-OUTRA-NATUREZA']
        choice = [
            'MEST',
            'POS-DOC',
            'TCC',
            'IC',
            'DOUT',
            'MONO-ESP',
            'OUTRA']
        df['NATURE'] = np.select(cond, choice, '-99')
        # group by fullname nature
        adv_gbfullname_nature = df.groupby(
            ['INSTITUTION', 'PUPIL', 'NATURE'])['TITLE'].size() \
            .unstack().reset_index(drop=False)
        adv_gbfullname_nature = adv_gbfullname_nature.reset_index(drop=True)
        adv_gbfullname_nature.fillna(0, inplace=True)
        advsum0 = adv_gbfullname_nature.iloc[:, 2:].sum(axis=0).to_list()
        advsum0.insert(0, '-')
        advsum0.insert(0, 'Total')
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature.columns))
        adv_gbfullname_nature = pd.concat([adv_gbfullname_nature, x], axis=0)
        adv_gbfullname_nature_table = tabulate(
            adv_gbfullname_nature, headers="keys", tablefmt='html')
        if len(adv_gbfullname_nature) >= 2:
            return adv_gbfullname_nature_table
        else:
            return '<b>Não há orientações concluidas para o pesquisador.</b><br>'
    else:
        return '<b>Não há orientações concluídas para o pesquisador.</b>'


def report_resch_advi_runn_each(idlattes, rep_setup_file):
    """Return table with all advising summary production for each researcher."""
    if rep_setup_file['advisrunn_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advisrunn_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        df = df.reset_index(drop=True)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        # replace categories names in nature column
        colname = 'NATURE'
        cond = [
            df[colname] == 'Dissertação de mestrado',
            df[colname] == 'Supervisão de pós-doutorado',
            df[colname] == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO',
            df[colname] == 'Iniciação Científica',
            df[colname] == 'Tese de doutorado',
            df[colname] == 'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO',
            df[colname] == 'Orientação de outra natureza']
        choice = [
            'MEST',
            'POS-DOC',
            'TCC',
            'IC',
            'DOUT',
            'MONO-ESP',
            'OUTRA']
        df['NATURE'] = np.select(cond, choice, '-99')
        # group by fullname nature
        adv_gbfullname_nature = df.groupby(
            ['INSTITUTION', 'PUPIL', 'NATURE'])['TITLE'].size() \
            .unstack().reset_index(drop=False)
        adv_gbfullname_nature = adv_gbfullname_nature.reset_index(drop=True)
        adv_gbfullname_nature.fillna(0, inplace=True)
        advsum0 = adv_gbfullname_nature.iloc[:, 2:].sum(axis=0).to_list()
        advsum0.insert(0, '-')
        advsum0.insert(0, 'Total')
        advsum0
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature.columns))
        adv_gbfullname_nature = pd.concat([adv_gbfullname_nature, x], axis=0)
        adv_gbfullname_nature_table = tabulate(
            adv_gbfullname_nature, headers="keys", tablefmt='html')
        if len(adv_gbfullname_nature) >= 2:
            return adv_gbfullname_nature_table
        else:
            return '<b>Não há orientações em andamento para o pesquisador.</b><br>'
    else:
        return '<b>Não há orientações em andamento para o pesquisador.</b><br>'


def report_resch_ppe(idlattes, rep_setup_file):
    """Return a table with projects activties for a researcher."""
    if rep_setup_file['ppe_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_ppe_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        if len(df) >= 1:
            df.reset_index(inplace=True, drop=True)
            df = df.loc[:, ['TITLE', 'NATURE', 'YEAR', 'YEAR_FIN',
                            'COORDINATOR', 'MEMBERS', 'FULL_NAME']]
            df.reset_index(inplace=True, drop=True)
            # proj research
            dfgb_natu = df.groupby(['NATURE', 'YEAR', 'YEAR_FIN', 'TITLE',
                                    'COORDINATOR'])['TITLE'].size().unstack()
            dfgb_natu = dfgb_natu.fillna(0)
            lscols = list(dfgb_natu.columns)
            len(lscols)
            dfgb_natu.reset_index(inplace=True, drop=False)
            # dfgb_natu
            if len(lscols) == 1:
                coord0 = np.sum([dfgb_natu.iloc[idw].loc[lscols[0]]
                                 for idw in range(len(dfgb_natu))])
                x = pd.DataFrame([np.transpose(['-', '-', '-', 'Total',
                                                coord0])],
                                 columns=list(dfgb_natu.columns))
                dfgb_natu = pd.concat([dfgb_natu, x], axis=0)
            else:
                coord0 = np.sum([dfgb_natu.iloc[idw].loc[lscols[0]]
                                 for idw in range(len(dfgb_natu))])
                coord1 = np.sum([dfgb_natu.iloc[idw].loc[lscols[1]]
                                 for idw in range(len(dfgb_natu))])
                x = pd.DataFrame([np.transpose(['-', '-', '-',
                                                'Total', coord0, coord1])],
                                 columns=list(dfgb_natu.columns))
                dfgb_natu = pd.concat([dfgb_natu, x], axis=0)
                dfgb_natu
            dfgb_natu.reset_index(inplace=True, drop=True)
            tablhtml = tabulate(dfgb_natu, headers='keys', tablefmt='html')
            return tablhtml
        else:
            return '<b>Não há projetos para o pesquisador.</b>'
    else:
        return '<b>Não há projetos para o pesquisador.</b>'


def report_resch_books(idlattes, rep_setup_file):
    """Return a table with books production for a researcher."""
    if rep_setup_file['books_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_books_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        df.reset_index(inplace=True, drop=True)
        dfgb_year = df.groupby(
            ['YEAR', 'TITLE'])['ID'].size().reset_index(drop=False)
        dfgb_year = pd.concat(
            [dfgb_year,
             pd.DataFrame([['-', 'Total', dfgb_year['ID'].sum()]],
                          columns=list(dfgb_year.columns))], axis=0)
        lsnewcolumns = list(dfgb_year.columns)
        lsnewcolumns[-1] = 'AMOUNT'
        dfgb_year.columns = lsnewcolumns
        dfgb_year.reset_index(inplace=True, drop=True)
        if len(dfgb_year) >= 2:
            tablhtml = tabulate(dfgb_year, headers='keys', tablefmt='html')
            return tablhtml
        else:
            return '<b>Não há livros para o pesquisador.</b>'
    else:
        return '<b>Não há livros para o pesquisador.</b>'


def report_resch_chapters(idlattes, rep_setup_file):
    """Return a table with chapters production for a researcher."""
    if rep_setup_file['chapters_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_chapters_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        df.reset_index(inplace=True, drop=True)
        dfgb_year = df.groupby(
            ['YEAR', 'TITLE'])['ID'].size().reset_index(drop=False)
        dfgb_year = pd.concat(
            [dfgb_year,
             pd.DataFrame([['-', 'Total', dfgb_year['ID'].sum()]],
                          columns=list(dfgb_year.columns))], axis=0)
        lsnewcolumns = list(dfgb_year.columns)
        lsnewcolumns[-1] = 'AMOUNT'
        dfgb_year.columns = lsnewcolumns
        dfgb_year.reset_index(inplace=True, drop=True)
        if len(dfgb_year) >= 2:
            tablhtml = tabulate(dfgb_year, headers='keys', tablefmt='html')
            return tablhtml
        else:
            return '<b>Não há capítulos para o pesquisador.</b>'
    else:
        return '<b>Não há capítulos para o pesquisador.</b>'


def report_resch_papers(idlattes, rep_setup_file):
    """Return a table with papers production for a researcher."""
    if rep_setup_file['papers_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_papers_all.csv',
                         header=0, dtype=str)
        df = df[df['ID'] == idlattes]
        df.reset_index(inplace=True, drop=True)
        dfgb_year = df.groupby(
            ['TITLE', 'JOURNAL', 'QUALIS'])['ID'].size().unstack()  # reset_index(drop=False)
        dfgb_year = dfgb_year.fillna(0)
        # lscols = list(dfgb_year.columns)
        dfgb_year.reset_index(inplace=True, drop=False)
        # dfgb_year.reset_index(inplace=True, drop=False)
        lssum0 = dfgb_year.iloc[:, 2:].sum().to_list()
        lssum0.insert(0, 'Total')
        lssum0.insert(0, '-')
        dfgb_year = pd.concat(
            [dfgb_year, pd.DataFrame([np.transpose(lssum0)],
                                     columns=list(dfgb_year.columns))], axis=0)
        dfgb_year.reset_index(inplace=True, drop=True)
        if len(dfgb_year) >= 2:
            tablhtml = tabulate(dfgb_year, headers='keys', tablefmt='html')
            return tablhtml
        else:
            return '<b>Não há artigos para o pesquisador.</b>'
    else:
        return '<b>Não há artigos para o pesquisador.</b>'


def report_resch_papers_group_all(rep_setup_file):
    """Return table with papers production for group with duplicate papers."""
    if rep_setup_file['papers_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_papers_all.csv',
                         header=0, dtype=str)
        papr_gbfullnamequal = df.groupby(
            ['FULL_NAME', 'QUALIS'])['TITLE'].size().unstack().reset_index(
                drop=False)
        papr_gbfullnamequal.fillna(0, inplace=True)
        papr_gbfullnamequal['TOTAL'] = papr_gbfullnamequal.iloc[:, 1:].sum(
            axis=1)
        papr_gbfullnamequal.reset_index(inplace=True, drop=True)
        # lstot = papr_gbfullnamequal.iloc[:, 1:].sum(axis=0).to_list()
        # lstot.insert(0, 'Total')
        # papr_gbfullnamequal = pd.concat(
        #     [papr_gbfullnamequal,
        #      pd.DataFrame([lstot],
        #                   columns=list(papr_gbfullnamequal.columns))],
        #     axis=0).reset_index(drop=True)
        papr_gbfullnamequal_table = tabulate(papr_gbfullnamequal,
                                             headers="keys", tablefmt='html')
        return papr_gbfullnamequal_table
    else:
        return '<b>Não há artigos para o grupo.</b>'


def report_resch_papers_group_uniq(rep_setup_file):
    """Return table with papers production for group with duplicate papers."""
    if rep_setup_file['papers_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_papers_uniq.csv',
                         header=0, dtype=str)
        papr_gbfullnamequal = df.groupby(
            ['FULL_NAME', 'QUALIS'])['TITLE'].size().unstack().reset_index(
                drop=False)
        papr_gbfullnamequal.fillna(0, inplace=True)
        papr_gbfullnamequal['TOTAL'] = papr_gbfullnamequal.iloc[:, 1:].sum(
            axis=1)
        papr_gbfullnamequal.reset_index(inplace=True, drop=True)
        lstot = papr_gbfullnamequal.iloc[:, 1:].sum(axis=0).to_list()
        lstot.insert(0, 'Total')
        papr_gbfullnamequal = pd.concat(
            [papr_gbfullnamequal,
             pd.DataFrame([lstot],
                          columns=list(papr_gbfullnamequal.columns))],
            axis=0).reset_index(drop=True)
        papr_gbfullnamequal_table = tabulate(papr_gbfullnamequal,
                                             headers="keys", tablefmt='html')
        return papr_gbfullnamequal_table
    else:
        return '<b>Não há artigos para o grupo.</b>'


def report_resch_advi_done_pg(rep_setup_file, pgname):
    """Return table with done advising summary for all for assigned PG."""
    if rep_setup_file['advis_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advis_all.csv',
                         header=0, dtype=str)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        df = df[(df['NATURE'] == 'Dissertação de mestrado') |
                (df['NATURE'] == 'Tese de doutorado')]
        # filter for pg name
        df = df.reset_index(drop=True)
        lspgname = pgname.split(' ')
        lspgname_rmitem = []
        for item in lspgname:
            if len(item) <= 2:
                lspgname_rmitem.append(item)
        [lspgname.remove(dd) for dd in lspgname_rmitem]
        lspgfilter = []
        for idx in range(len(df)):
            lscourse = df['COURSE'].iloc[idx]
            lscourse = lscourse.split(' ')
            lscourse_rmitem = []
            for item in lscourse:
                if len(item) <= 2:
                    lscourse_rmitem.append(item)
            [lscourse.remove(dd) for dd in lscourse_rmitem]
            if len(set(lspgname) & set(lscourse)) >= 2:
                lspgfilter.append('YES')
            else:
                lspgfilter.append('NO')
        df['PG_YESNO'] = lspgfilter
        df = df[df['PG_YESNO'] == 'YES']
        df = df.reset_index(drop=True)
        # group by fullname nature
        adv_gbfullname_nature_year = df.groupby(
            ['FULL_NAME', 'NATURE'])['TITLE'].size() \
            .unstack() \
            .reset_index(drop=False)
        adv_gbfullname_nature_year
        adv_gbfullname_nature_year.fillna(0, inplace=True)
        adv_gbfullname_nature_year['TOTAL'] = adv_gbfullname_nature_year \
            .iloc[:, 1:] \
            .sum(axis=1)
        advsum0 = adv_gbfullname_nature_year.iloc[:, 1:].sum(axis=0).to_list()
        advsum0.insert(0, 'Total')
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature_year.columns))
        adv_gbfullname_nature_year = pd.concat([adv_gbfullname_nature_year,
                                                x], axis=0)
        adv_gbfullname_nature_year_table = tabulate(
            adv_gbfullname_nature_year,
            headers="keys", tablefmt='html')
        return adv_gbfullname_nature_year_table
    else:
        return '<b>Não há orientações concluídas para o grupo.</b>'


def report_resch_advi_runn_pg(rep_setup_file, pgname):
    """Return table with running advising summary for all for assigned PG."""
    if rep_setup_file['advisrunn_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advisrunn_all.csv',
                         header=0, dtype=str)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        df = df[(df['NATURE'] == 'Dissertação de mestrado') |
                (df['NATURE'] == 'Tese de doutorado')]
        # filter for pg name
        df = df.reset_index(drop=True)
        lspgname = pgname.split(' ')
        lspgname_rmitem = []
        for item in lspgname:
            if len(item) <= 2:
                lspgname_rmitem.append(item)
        [lspgname.remove(dd) for dd in lspgname_rmitem]
        lspgfilter = []
        for idx in range(len(df)):
            lscourse = df['COURSE'].iloc[idx]
            lscourse = lscourse.split(' ')
            lscourse_rmitem = []
            for item in lscourse:
                if len(item) <= 2:
                    lscourse_rmitem.append(item)
            [lscourse.remove(dd) for dd in lscourse_rmitem]
            if len(set(lspgname) & set(lscourse)) >= 2:
                lspgfilter.append('YES')
            else:
                lspgfilter.append('NO')
        df['PG_YESNO'] = lspgfilter
        df = df[df['PG_YESNO'] == 'YES']
        df = df.reset_index(drop=True)
        # group by fullname nature
        adv_gbfullname_nature_year = df.groupby(
            ['FULL_NAME', 'NATURE'])['TITLE'].size() \
            .unstack() \
            .reset_index(drop=False)
        adv_gbfullname_nature_year
        adv_gbfullname_nature_year.fillna(0, inplace=True)
        adv_gbfullname_nature_year['TOTAL'] = adv_gbfullname_nature_year \
            .iloc[:, 1:] \
            .sum(axis=1)
        advsum0 = adv_gbfullname_nature_year.iloc[:, 1:].sum(axis=0).to_list()
        advsum0.insert(0, 'Total')
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature_year.columns))
        adv_gbfullname_nature_year = pd.concat([adv_gbfullname_nature_year,
                                                x], axis=0)
        adv_gbfullname_nature_year_table = tabulate(
            adv_gbfullname_nature_year,
            headers="keys", tablefmt='html')
        return adv_gbfullname_nature_year_table
    else:
        return '<b>Não há orientações em andamento para o grupo.</b>'


def report_resch_advi_done_all(rep_setup_file):
    """Return table with all advising summary production for all researches."""
    if rep_setup_file['advis_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advis_all.csv',
                         header=0, dtype=str)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        # replace categories names in nature column
        colname = 'NATURE'
        cond = [
            df[colname] == 'Dissertação de mestrado',
            df[colname] == 'Supervisão de pós-doutorado',
            df[colname] == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO',
            df[colname] == 'INICIACAO_CIENTIFICA',
            df[colname] == 'Tese de doutorado',
            df[colname] == 'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO',
            df[colname] == 'ORIENTACAO-DE-OUTRA-NATUREZA']
        choice = [
            'MEST',
            'POS-DOC',
            'TCC',
            'IC',
            'DOUT',
            'MONO-ESP',
            'OUTRA']
        df['NATURE'] = np.select(cond, choice, '-99')
        # group by fullname nature
        adv_gbfullname_nature = df.groupby(
            ['FULL_NAME', 'NATURE'])['TITLE'].size() \
            .unstack() \
            .reset_index(drop=False)
        adv_gbfullname_nature
        adv_gbfullname_nature.fillna(0, inplace=True)
        adv_gbfullname_nature['TOTAL'] = adv_gbfullname_nature.iloc[:, 1:] \
                                                              .sum(axis=1)
        advsum0 = adv_gbfullname_nature.iloc[:, 1:].sum(axis=0).to_list()
        advsum0.insert(0, 'Total')
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature.columns))
        adv_gbfullname_nature = pd.concat([adv_gbfullname_nature,
                                           x], axis=0)

        adv_gbfullname_nature_table = tabulate(
            adv_gbfullname_nature, headers="keys", tablefmt='html')
        return adv_gbfullname_nature_table
    else:
        return '<b>Não há orientações concluídas para o grupo.</b>'


def report_resch_advi_runn_all(rep_setup_file):
    """Return table with all running advising summary production for all researches."""
    if rep_setup_file['advisrunn_all']['print'] == 'YES':
        df = pd.read_csv('./relatorio/csv_report/report_advisrunn_all.csv',
                         header=0, dtype=str)
        df['YEAR'] = df['YEAR'].apply(lambda x: int(x))
        # replace categories names in nature column
        colname = 'NATURE'
        cond = [
            df[colname] == 'Dissertação de mestrado',
            df[colname] == 'Supervisão de pós-doutorado',
            df[colname] == 'TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO',
            df[colname] == 'Iniciação Científica',
            df[colname] == 'Tese de doutorado',
            df[colname] == 'MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO',
            df[colname] == 'Orientação de outra natureza']
        choice = [
            'MEST',
            'POS-DOC',
            'TCC',
            'IC',
            'DOUT',
            'MONO-ESP',
            'OUTRA']
        df['NATURE'] = np.select(cond, choice, '-99')
        # group by fullname nature
        adv_gbfullname_nature = df.groupby(
            ['FULL_NAME', 'NATURE'])['TITLE'].size() \
            .unstack() \
            .reset_index(drop=False)
        adv_gbfullname_nature
        adv_gbfullname_nature.fillna(0, inplace=True)
        adv_gbfullname_nature['TOTAL'] = adv_gbfullname_nature.iloc[:, 1:] \
                                                              .sum(axis=1)
        advsum0 = adv_gbfullname_nature.iloc[:, 1:].sum(axis=0).to_list()
        advsum0.insert(0, 'Total')
        x = pd.DataFrame([np.transpose(advsum0)],
                         columns=list(adv_gbfullname_nature.columns))
        adv_gbfullname_nature = pd.concat([adv_gbfullname_nature,
                                           x], axis=0)

        adv_gbfullname_nature_table = tabulate(
            adv_gbfullname_nature, headers="keys", tablefmt='html')
        return adv_gbfullname_nature_table
    else:
        return '<b>Não há orientações em andamento para o grupo.</b>'


def report_tbl_indexh(rep_setup_file):
    """Return table and save a plot for index x for all researchers."""
    if rep_setup_file['hwebofsci']['print'] == 'YES':
        df = pd.read_csv(
            './csv_producao_hindex/hindex_websci_papers_tbl.csv',
            header=0, dtype='str')
        tab = df.loc[:, ['FULL_NAME', 'HWEBSCI', 'TOTAL_PUBLIC',
                         'TOTAL_CITATION', 'CITATION_AVR']]
        tab.columns = ['NOME', 'IND H_woc ', 'TOTAL PUBLICAC',
                       'TOTAL CITACAO', 'CITACAO MEDIA']
        tab = tabulate(tab, headers='keys', tablefmt='html', showindex=True)
        return tab
    else:
        return '<b>Não há índice H - base webofknowledge <br>\n.</b>'


def report_tbl_indexh_uniq(rep_setup_file):
    """Return table and save a plot for index x for all researchers."""
    if rep_setup_file['hwebofsci']['print'] == 'YES':
        df = pd.read_csv(
            './csv_producao_hindex/hindex_websci_papers_tbl_uniq.csv',
            header=0, dtype='str')
        tab = df.loc[:, ['FULL_NAME', 'HWEBSCI', 'TOTAL_PUBLIC',
                         'TOTAL_CITATION', 'CITATION_AVR']]
        tab.columns = ['NOME', 'IND H_woc ', 'TOTAL PUBLICAC',
                       'TOTAL CITACAO', 'CITACAO MEDIA']
        tab = tabulate(tab, headers='keys', tablefmt='html', showindex=True)
        return tab
    else:
        return '<b>Não há índice H - base webofknowledge <br>\n.</b>'


def report_tbl_indexh_group_paper_summary():
    """Return table with a summary for group index h."""
    df = pd.read_csv(
        './csv_producao_hindex/hindex_websci_allgroup_papers_summary.csv',
        header=0, dtype='str')
    df.columns = ['IND H_woc ', 'TOTAL PUBLICAC',
                  'TOTAL CITACAO', 'CITACAO MEDIA']
    tab = tabulate(df, headers='keys', tablefmt='html', showindex=True)
    return tab


def report_tbl_indexh_group_paper_report():
    """Return table with a report for papers of the group."""
    df = pd.read_csv(
        './csv_producao_hindex/hindex_websci_allgroup_papers_report.csv',
        header=0, dtype='str')
    tab = tabulate(df, headers='keys', tablefmt='html', showindex=True)
    return tab
