# remove csv files into ./csv_producao

import os
import glob


def removeCsvProducao():
    fileToRemove = glob.glob('./csv_producao/*.csv')

    for ff in fileToRemove:
        try:
            os.remove(ff)
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))
