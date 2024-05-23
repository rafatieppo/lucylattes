"""Analize procuction files, create a csv setup file, filter production by \
year."""

import json
# import datetime as dt
# import numpy as np
import pandas as pd
# from resources.support_functions import yearlimit_forfilter
from resources.report_class_filteryear import FilterYears
from resources.report_setup_dict import report_setup_dict_base


def report_setup_json():
    """Analize procuction files, create setup file, csv to generat report."""
    # lsyear_limits = yearlimit_forfilter()

    dicreport_setup = report_setup_dict_base()
    # print(dicreport_setup)
    lsfiles_toreport = list(dicreport_setup)

    for production in lsfiles_toreport:
        try:
            df = pd.read_csv(dicreport_setup[production]['pathfilename'],
                             header=0, dtype='str')
        except (OSError, IOError):
            print('------------------------------------------------------------\n' +
                  'ATTENTION \n' +
                  'There is NO ' + dicreport_setup[production]['pathfilename'] + '\n' +
                  '------------------------------------------------------------')
            dicreport_setup[production].update({'print': 'NO'})
        else:
            # dicreport_setup[production].update({'print': 'YES'})
            filterYear = FilterYears(dicreport_setup, production)
            filterYear.return_func(df)

    with open('./relatorio/report_setup.json', 'w') as convert_file:
        convert_file.write(json.dumps(dicreport_setup))
        convert_file.close()
