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
from readidlist import readIdList
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

gettidydf()
getverificacao()
getgrapho()
getrelatorio()
