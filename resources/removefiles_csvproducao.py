"""Remove csv file in several folders."""

import os
import glob


def remove_csv_producao():
    """
    Remove csv file in folders.

    Remove csv file in ./csv_producao ./relatorio/csv_report
    folder and ./csv_producao_hindex.
    """
    fileToRemove = glob.glob('./csv_producao/*.csv')
    for ff in fileToRemove:
        try:
            os.remove(ff)
            # print('./csv_producao/*.csv has been removed')
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))

    fileToRemove = glob.glob('./relatorio/csv_report/*.csv')
    for ff in fileToRemove:
        try:
            os.remove(ff)
            # print('./relatorio/csv_report/*.csv has been removed')
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))

    fileToRemove = glob.glob('./csv_producao_hindex/*.csv')
    for ff in fileToRemove:
        try:
            os.remove(ff)
            # print('./csv_producao_hindex/*.csv has been removed')
        except OSError as e:
            print("Error: %s : %s" % (ff, e.strerror))
