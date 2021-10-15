# ======================================================================
# Rafael Tieppo
# rafaeltieppo@yahoo.com.br
# https://rafatieppo.github.io/
# 16-01-2019
# LATTES Scraper
# @rafatieppo
# ======================================================================

# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

from tidydf import *
from extrafuns import *
from report import getrelatorio
from grapho import getgrapho
from verify import getverificacao
from scraperlattes import getnomecompleto
from scraperlattes import getcapit
from scraperlattes import getlivro
from scraperlattes import getperiod
from scraperlattes import getorient
from scraperlattes import getprodtec
from scraperlattes import getprojpesqext
from scraperlattes import getdiscip
from readidlist import readIdList
from index_capes import capes_indprodart
from index_capes import capes_indori
from index_capes import capes_indautdis
from index_capes import capes_distindproddp
from remove_csvproducao import removeCsvProducao
from tabulate import tabulate
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

# ------------------------------------------------------------
# lendo a lista dos IDs e nome dos pesquisadores

df_idlist = readIdList()

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
    getdiscip(zipfilename)

gettidydf()
getverificacao()
getgrapho()

# Gerar indicadores qualis ou nao
# config_file = open('./config.txt', 'r')
config_file = open('./config.txt', 'r', encoding='utf-8')
run_indcapes = config_file.readlines()[7].split(':')[1]
run_indcapes = run_indcapes.rstrip('\n')
run_indcapes = run_indcapes.strip(' ')
run_indcapes = int(run_indcapes)
run_indcapes
config_file.close()
if run_indcapes == 1:
    capes_indori()
    capes_indprodart()
    capes_indautdis()
    capes_distindproddp()
else:
    print("Indicadores capes para PPG nao foram gerados")

getrelatorio()
removeCsvProducao()
