# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

import numpy as np
import pandas as pd
import os
import glob
import re

# ------------------------------------------------------------
# Funcoes
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
