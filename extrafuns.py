# ------------------------------------------------------------
# packages
# ------------------------------------------------------------
# ------------------------------------------------------------
import numpy as np
import pandas as pd
import os
import glob
import re
import platform
# ------------------------------------------------------------
# Funcoes gerais
# ------------------------------------------------------------


def ss(x): return str(x)


def ff(x): return float(x)


def iint(x): return int(x)


def fun_result(x):
    if x is None:
        cc = 'VAZIO'
    else:
        cc = x.group(1)
    return cc


def fun_uppercase(x):
    x = x.upper()
    return x


def fun_idd_unixwind(psys, lscsv, count):
    if psys == 'Windows':
        sp = str(lscsv[count].split('_')[1].split('\\')[1])
    else:
        sp = str(lscsv[count].split('_')[1].split('/')[1])
    return sp


# ------------------------------------------------------------
# Funcoes index capes
# ------------------------------------------------------------

# nome ppg


def fun_nomeppg():
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    name_ppg = config_file.readlines()[8].split(':')[1]
    name_ppg = name_ppg.rstrip('\n')
    name_ppg = name_ppg.strip(' ')
    name_ppg = fun_uppercase(name_ppg)
    config_file.close()
    return name_ppg


# identificando os ppg dos pesquisadores
def fun_ppgs():
    df = pd.read_csv('./csv_producao/orientacoes_all.csv',
                     header=0, sep=',')
    df = df.query('NATURE == "Dissertação de mestrado" \
                   or NATURE == "Tese de doutorado"')
    df = df.query('TYPE != "CO_ORIENTADOR"').reset_index(drop=True)
    df['COURSE'] = df['COURSE'].apply(fun_uppercase)
    ls_ppgs = df['COURSE'].unique()
    ls_ppgs.sort()
    ls_ppgs = ", ".join(ls_ppgs)
    return ls_ppgs


# indori

def fun_peso_defesa(x):
    if x == 'Dissertação de mestrado':
        pes = 1
    elif x == 'Tese de doutorado':
        pes = 2
    else:
        pes = 0
    return pes


def fun_indori_classif(x):
    if x < 0.15:
        classif = 'DEFICIENTE'
    elif x >= 0.15 and x <= 0.29:
        classif = 'FRACO'
    elif x > 0.29 and x <= 0.79:
        classif = 'REGULAR'
    elif x > 0.79 and x <= 1.19:
        classif = 'BOM'
    else:
        classif = 'MUITO_BOM'
    return classif

# indprodart


def fun_indprodart_classif(x):
    if x == 'A1':
        classif = 1
    elif x == 'A2':
        classif = 0.85
    elif x == 'B1':
        classif = 0.7
    elif x == 'B2':
        classif = 0.55
    elif x == 'B3':
        classif = 0.4
    elif x == 'B4':
        classif = 0.25
    elif x == 'B5':
        classif = 0.1
    else:
        classif = 0
    return classif
