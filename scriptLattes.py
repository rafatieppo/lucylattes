# ======================================================================
# Rafael Tieppo
# rafaeltieppo@yahoo.com.br
# https://rafatieppo.github.io/
# 16-01-2019
# LATTES Scraper
# ======================================================================

# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile

# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.style as style
# style.available
# style.use('fivethirtyeight')
# sns.set_style('whitegrid')

# ------------------------------------------------------------
# lendo a lista dos IDs e nome dos pesquisadores

from readidlist import readIdList
df_idlist = readIdList()
df_idlist
len(df_idlist)

# ------------------------------------------------------------
# carregar funções

from parserlattes import getprojpesqext
from parserlattes import getprodtec
from parserlattes import getorient
from parserlattes import getperiod

# ------------------------------------------------------------
# roda as funcoes para pegar dados de cada pesquisador

for nid in range(len(df_idlist)):
    zipfilename = str(df_idlist.iloc[nid, 0]) + '.zip'
    getprojpesqext(zipfilename)
    getprodtec(zipfilename)
    getorient(zipfilename)
    getperiod(zipfilename)

z
# ------------------------------------------------------------
# lendo arquivo gerado pelo script lattes
# ------------------------------------------------------------
# os.listdir('.')
# infile = open("./curriculo.xml", "r", encoding='ISO-8859-1')
# infile = open("./curriculo_riva.xml", "r", encoding='ISO-8859-1')
# contents = infile.read()
# soup = BeautifulSoup(contents, 'lxml')
