"""Tidy all csv files and join it in only on csv for each production."""

import glob
import pandas as pd
import re
from resources.support_functions import droprow_nullyear
from resources.tidydata_uniq_titles import clean_titles
from resources.tidydata_uniq_titles import get_uniq_titles
# import platform
# from resources.support_functions import yearlimit_forfilter


def concat_df(df0, df1):
    """Concat 2 pandas df."""
    dfconcat = pd.concat([df0, df1], axis=0, ignore_index=False)
    return dfconcat


def tidydata_ppe():
    """Tidy all ppe csv files and join it in only one csv - all and uniq."""
    # df research and extension projects
    lscsv_ppe = glob.glob('./csv_producao/*_ppe.csv')
    if len(lscsv_ppe) == 0:
        print('There is NO any xxxxx_ppe.csv file')
    else:
        df_ppe = pd.DataFrame()
        for idx in range(len(lscsv_ppe)):
            df = pd.read_csv(lscsv_ppe[idx], header=0, dtype='str')
            # df_ppe = df_ppe.append(df, ignore_index=False)
            df_ppe = concat_df(df_ppe, df)
        df_ppe.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_ppe on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_ppe = pd.merge(df_ppe, df_fullname, on='ID')
        df_ppe.reset_index(inplace=True, drop=True)
        # remove all lines with VAZIO title
        df_ppe = df_ppe.query('TITLE != "VAZIO"')
        df_ppe.reset_index(inplace=True, drop=True)
        df_ppe = df_ppe.query('MEMBERS != "VAZIO"')
        df_ppe.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_ppe.copy()
        df_ppe = droprow_nullyear(df)
        # rm dup proj and verify the owner by coordinator and author order
        lsmemberorder = []
        lscoordenate = []
        for idx in range(len(df_ppe['ID'])):
            fullname = df_ppe['FULL_NAME'].iloc[idx]
            lsmembers = df_ppe['MEMBERS'].iloc[idx]
            lsmembers = re.sub(r'(\[|\]|\')', '', lsmembers)
            lsmembers = lsmembers.replace(', ', ',')
            lsmembers = lsmembers.split(',')
            lscoordena = df_ppe['COORDENA'].iloc[idx]
            lscoordena = re.sub(r'(\[|\]|\')', '', lscoordena)
            lscoordena = lscoordena.replace(', ', ',')
            lscoordena = lscoordena.split(',')
            memberorder = -99
            for idy in range(len(lsmembers)):
                if fullname == lsmembers[idy]:
                    memberorder = idy + 1
            lsmemberorder.append(memberorder)
            # condicao para 1 pessoal no proj
            if memberorder == -99:
                lscoordenate.append(lscoordena[0])
            else:
                lscoordenate.append(lscoordena[memberorder-1])
        df_ppe = df_ppe.copy()
        df_ppe['MEMBER_ORDER'] = lsmemberorder
        df_ppe['COORDINATOR'] = lscoordenate
        lsorder = []
        for idx in range(len(df_ppe)):
            if df_ppe['COORDINATOR'].iloc[idx] == 'SIM':
                lsorder.append(0)
            else:
                lsorder.append(df_ppe['MEMBER_ORDER'].iloc[idx])
        df_ppe['ORDER_OK'] = lsorder
        df_ppe.reset_index(inplace=True, drop=True)
        # drop duplicate projs
        df_ppe_uniq = get_uniq_titles(df_ppe, 'TITLE', 1, 1, 0.9)
        # sort by id year
        df_ppe.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_ppe.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = './csv_producao/ppe_all.csv'
        df_ppe.to_csv(pathfilename, index=False)
        print(pathfilename,
              ' writed with ', len(df_ppe['TITLE']), ' projects')
        pathfilename = './csv_producao/ppe_uniq.csv'
        df_ppe_uniq.to_csv(pathfilename, index=False)
        print(pathfilename,
              ' writed with', len(df_ppe_uniq['TITLE']), ' projects')


def tidydata_worksevents():
    """Tidy all worksevents csv files and join it in only one csv - all and uniq."""
    # df papers
    lscsv_workevnt = glob.glob('./csv_producao/*_worksevents.csv')
    if len(lscsv_workevnt) == 0:
        print('There is NO any xxxxx_worksevents.csv file')
    else:
        df_workevnt = pd.DataFrame()
        for idx in range(len(lscsv_workevnt)):
            df = pd.read_csv(lscsv_workevnt[idx], header=0, dtype='str')
            # df_workevnt = df_workevnt.append(df, ignore_index=False)
            df_workevnt = concat_df(df_workevnt, df)
        df_workevnt.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_workevnt on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_workevnt = pd.merge(df_workevnt, df_fullname, on='ID')
        df_workevnt.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_workevnt.copy()
        df_workevnt = droprow_nullyear(df)
        # rm dup paper and verify the owner by author order
        # author order is already done from df_workevnt['ORDER_OK']
        df_workevnt_uniq = get_uniq_titles(df_workevnt, 'TITLE', 1, 1, 0.9)
        # sort by id year
        df_workevnt.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_workevnt.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/worksevents_all.csv')
        df_workevnt.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_workevnt['TITLE']), ' worksevents')
        pathfilename = str('./csv_producao/worksevents_uniq.csv')
        df_workevnt_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with',
              len(df_workevnt_uniq['TITLE']), ' worksevents')


def tidydata_papers():
    """Tidy all papers csv files and join it in only one csv - all and uniq."""
    # df papers
    lscsv_paper = glob.glob('./csv_producao/*_papers.csv')
    if len(lscsv_paper) == 0:
        print('There is NO any xxxxx_papers.csv file')
    else:
        df_paper = pd.DataFrame()
        for idx in range(len(lscsv_paper)):
            df = pd.read_csv(lscsv_paper[idx], header=0, dtype='str')
            # df_paper = df_paper.append(df, ignore_index=False)
            df_paper = concat_df(df_paper, df)
        df_paper.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_paper on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_paper = pd.merge(df_paper, df_fullname, on='ID')
        df_paper.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_paper.copy()
        df_paper = droprow_nullyear(df)
        # rm dup paper and verify the owner by author order
        # author order is already done from df_paper['ORDER_OK']
        df_paper_uniq = get_uniq_titles(df_paper, 'TITLE', 1, 1, 0.9)
        # sort by id year
        df_paper.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_paper.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = './csv_producao/papers_all.csv'
        df_paper.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_paper['TITLE']), ' papers')
        pathfilename = './csv_producao/papers_uniq.csv'
        df_paper_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with',
              len(df_paper_uniq['TITLE']), ' papers')


def tidydata_books():
    """Tidy all books csv files and join it in only one csv - all and uniq."""
    # df book
    lscsv_book = glob.glob('./csv_producao/*_books.csv')
    if len(lscsv_book) == 0:
        print('There is NO any xxxxx_books.csv file')
    else:
        df_book = pd.DataFrame()
        for idx in range(len(lscsv_book)):
            df = pd.read_csv(lscsv_book[idx], header=0, dtype='str')
            # df_book = df_book.append(df, ignore_index=False)
            df_book = concat_df(df_book, df)
        df_book.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_book on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_book = pd.merge(df_book, df_fullname, on='ID')
        df_book.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_book.copy()
        df_book = droprow_nullyear(df)
        # rm dup paper and verify the owner by author order
        # author order is already done from df_book['ORDER_OK']
        df_book_uniq = get_uniq_titles(df_book, 'TITLE', 1, 1, 0.9)
        # sort by id year
        df_book.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_book.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/books_all.csv')
        df_book.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_book['TITLE']), ' books')
        pathfilename = str('./csv_producao/books_uniq.csv')
        df_book_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with',
              len(df_book_uniq['TITLE']), ' books')


def tidydata_chapters():
    """Tidy all books csv files and join it in only one csv - all and uniq."""
    # df chap
    lscsv_chap = glob.glob('./csv_producao/*_chapters.csv')
    if len(lscsv_chap) == 0:
        print('There is NO any xxxxx_chapters.csv file')
    else:
        df_chap = pd.DataFrame()
        for idx in range(len(lscsv_chap)):
            df = pd.read_csv(lscsv_chap[idx], header=0, dtype='str')
            # df_chap = df_chap.append(df, ignore_index=False)
            df_chap = concat_df(df_chap, df)
        df_chap.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_chap on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_chap = pd.merge(df_chap, df_fullname, on='ID')
        df_chap.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_chap.copy()
        df_chap = droprow_nullyear(df)
        # rm dup paper and verify the owner by author order
        # author order is already done from df_chap['ORDER_OK']
        df_chap_uniq = get_uniq_titles(df_chap, 'TITLE', 1, 1, 0.9)
        # sort by id year
        df_chap.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_chap.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/chapters_all.csv')
        df_chap.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_chap['TITLE']), ' chapters')
        pathfilename = str('./csv_producao/chapters_uniq.csv')
        df_chap_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with',
              len(df_chap_uniq['TITLE']), ' chapters')


def tidydata_advising():
    """Tidy all adiv csv files and join it in only one csv - all."""
    # df adv
    lscsv_advis = glob.glob('./csv_producao/*_advis.csv')
    if len(lscsv_advis) == 0:
        print('There is NO any xxxxx_advis.csv file')
    else:
        df_advis = pd.DataFrame()
        for idx in range(len(lscsv_advis)):
            df = pd.read_csv(lscsv_advis[idx], header=0, dtype='str')
            # df_advis = df_advis.append(df, ignore_index=False)
            df_advis = concat_df(df_advis, df)
        df_advis.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_advis on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idy in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idy], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_advis = pd.merge(df_advis, df_fullname, on='ID')
        df_advis.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_advis.copy()
        df_advis = droprow_nullyear(df)
        # sort by id year ini
        df_advis.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_advis.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/advis_all.csv')
        df_advis.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_advis['TITLE']), ' advising')


def tidydata_advisingrunn():
    """Tidy all adiv running csv files and join it in only one csv - all."""
    # df adv
    lscsv_advis = glob.glob('./csv_producao/*_advisrunn.csv')
    if len(lscsv_advis) == 0:
        print('There is NO any xxxxx_advisrunn.csv file')
    else:
        df_advis = pd.DataFrame()
        for idx in range(len(lscsv_advis)):
            df = pd.read_csv(lscsv_advis[idx], header=0, dtype='str')
            # df_advis = df_advis.append(df, ignore_index=False)
            df_advis = concat_df(df_advis, df)
        df_advis.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_advis on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idy in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idy], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_advis = pd.merge(df_advis, df_fullname, on='ID')
        df_advis.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_advis.copy()
        df_advis = droprow_nullyear(df)
        # sort by id year ini
        df_advis.sort_values(by=['ID', 'YEAR'], inplace=True)
        df_advis.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/advisrunn_all.csv')
        df_advis.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_advis['TITLE']), ' advisingrunn')


def tidydata_teaching():
    """Tidy all teaching csv files and join it in only one csv - all."""
    # df teach
    lscsv_teach = glob.glob('./csv_producao/*_teaching.csv')
    if len(lscsv_teach) == 0:
        print('There is NO any xxxxx_teaching.csv file')
    else:
        df_teach = pd.DataFrame()
        for idx in range(len(lscsv_teach)):
            df = pd.read_csv(lscsv_teach[idx], header=0, dtype='str')
            # df_teach = df_teach.append(df, ignore_index=False)
            df_teach = concat_df(df_teach, df)
        df_teach.reset_index(inplace=True, drop=True)
        # df fullname data and merge with df_teach on id
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        df_teach = pd.merge(df_teach, df_fullname, on='ID')
        df_teach.reset_index(inplace=True, drop=True)
        # remove all lines with VAZIO degree
        df_teach = df_teach.query('DEGREE != "VAZIO"')
        df_teach.reset_index(inplace=True, drop=True)
        # drop rows with NaN, or any errors in year column
        df = df_teach.copy()
        df_teach = droprow_nullyear(df)
        # sort by id year ini
        df_teach = df_teach.copy()
        df_teach.sort_values(by=['ID', 'YEAR', 'MONTH_INI'], inplace=True)
        df_teach.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/teaching_all.csv')
        df_teach.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_teach['DEGREE']), ' teaching')


def tidydata_fullname():
    """Tidy all fullname csv files and join it in only one csv - all."""
    # df fullname
    lscsv_fullname = glob.glob('./csv_producao/*_fullname.csv')
    if len(lscsv_fullname) == 0:
        print('There is NO any xxxxx_fullname.csv file')
    else:
        df_fullname = pd.DataFrame()
        for idx in range(len(lscsv_fullname)):
            df = pd.read_csv(lscsv_fullname[idx], header=0, dtype='str')
            # df_fullname = df_fullname.append(df, ignore_index=False)
            df_fullname = concat_df(df_fullname, df)
        df_fullname.reset_index(inplace=True, drop=True)
        # sort by id year ini
        df_fullname.sort_values(by=['ID'], inplace=True)
        df_fullname.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/fullname_all.csv')
        df_fullname.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(df_fullname['ID']), ' fullname')


def tidydata_productsppect():
    """Tidy all productsppect csv files and join it in only one csv - all."""
    # df fullname
    lscsv_products = glob.glob('./csv_producao/*ppe_prods_ct.csv')
    if len(lscsv_products) == 0:
        print('There is NO any xxxxx_ppe_prods_ct.csv file')
    else:
        dfproducts = pd.DataFrame()
        for idx in range(len(lscsv_products)):
            df = pd.read_csv(lscsv_products[idx], header=0, dtype='str')
            # dfproducts = dfproducts.append(df, ignore_index=False)
            dfproducts = concat_df(dfproducts, df)
        dfproducts.reset_index(inplace=True, drop=True)
        # sort by id year ini
        dfproducts.sort_values(by=['ID'], inplace=True)
        dfproducts.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/ppe_prods_ct_all.csv')
        dfproducts.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(dfproducts['ID']), 'producoes ct do projeto')


def tidydata_productsppeadv():
    """Tidy all productsppeadv csv files and join it in only one csv - all."""
    # df fullname
    lscsv_products = glob.glob('./csv_producao/*ppe_prods_adv.csv')
    if len(lscsv_products) == 0:
        print('There is NO any xxxxx_ppe_prods_adv.csv file')
    else:
        dfproducts = pd.DataFrame()
        for idx in range(len(lscsv_products)):
            df = pd.read_csv(lscsv_products[idx], header=0, dtype='str')
            # dfproducts = dfproducts.append(df, ignore_index=False)
            dfproducts = concat_df(dfproducts, df)
        dfproducts.reset_index(inplace=True, drop=True)
        # sort by id year ini
        dfproducts.sort_values(by=['ID'], inplace=True)
        dfproducts.reset_index(inplace=True, drop=True)
        # write files
        pathfilename = str('./csv_producao/ppe_prods_adv_all.csv')
        dfproducts.to_csv(pathfilename, index=False)
        print(pathfilename, ' writed with ',
              len(dfproducts['ID']), 'producoes adv do projeto')
