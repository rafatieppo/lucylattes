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

import glob
import re
import matplotlib.pyplot as plt
import matplotlib.style as style
# style.available
style.use('fivethirtyeight')
from tabulate import tabulate

# ------------------------------------------------------------
# lendo a lista dos IDs e nome dos pesquisadores

from readidlist import readIdList
df_idlist = readIdList()
# df_idlist
len(df_idlist)

# ------------------------------------------------------------
# carregar funções

from scraperlattes import getprojpesqext
from scraperlattes import getprodtec
from scraperlattes import getorient
from scraperlattes import getperiod
from scraperlattes import getlivro
from scraperlattes import getcapit
from scraperlattes import getnomecompleto
from grapho import getgrapho
from report import getrelatorio

from extrafuns import *
from tidydf import *

# ------------------------------------------------------------
# roda as funcoes para pegar dados de cada pesquisador

for nid in range(len(df_idlist)):
    zipfilename = str(df_idlist.iloc[nid, 0]) + '.zip'
    getprojpesqext(zipfilename)
    getprodtec(zipfilename)
    getorient(zipfilename)
    getperiod(zipfilename)
    getlivro(zipfilename)
    getcapit(zipfilename)
    getnomecompleto(zipfilename)

gettidydf()
getgrapho()
getrelatorio()

# z
# ------------------------------------------------------------
# lendo arquivo gerado pelo script lattes
# ------------------------------------------------------------
# os.listdir('.')
# infile = open("./curriculo.xml", "r", encoding='ISO-8859-1')
# infile = open("./curriculo_riva.xml", "r", encoding='ISO-8859-1')
# contents = infile.read()
# soup = BeautifulSoup(contents, 'lxml')
