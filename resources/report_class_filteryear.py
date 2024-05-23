"""A class to filter productions for report regarding year column name."""

import datetime as dt
import numpy as np
from resources.support_functions import yearlimit_forfilter
from resources.report_setup_dict import report_setup_dict_base


class FilterYears:
    """A class to filter productions for report regarding year column name."""

    def __init__(self, dicreport_setup, production):
        """Init method."""
        self.dicreport_setup = dicreport_setup
        self.production = production
        # self.df = df

    def column_yearfin(self, df):
        """Filter production by means columns year_fin and year_ini."""
        lsyear_limits = yearlimit_forfilter()
        current_year = dt.datetime.today()
        df['YEAR'] = [int(yy) for yy in df['YEAR'].to_list()]
        df['YEAR_FIN'] = [int(current_year.year) if yy ==
                          'ATUAL' else yy for yy in df['YEAR_FIN']]
        allowed_years = list(
            np.arange(lsyear_limits[0], lsyear_limits[1] + 1, 1))
        lsyear_inout = []
        for idx in range(len(df)):
            if len(list(set(list(np.arange(
                    df['YEAR'].iloc[idx],
                    int(df['YEAR_FIN'].iloc[idx]) + 1, 1)))
                    & set(allowed_years))) >= 1:
                lsyear_inout.append('IN')
            else:
                lsyear_inout.append('OUT')
        df['FILTER_YEAR'] = lsyear_inout
        df = df[df['FILTER_YEAR'] == 'IN']
        filename = self.dicreport_setup[
            self.production]['pathfilename'].split(
            '/')[-1]
        pathfilename = './relatorio/csv_report/' + 'report_' + filename
        if len(df) >= 1:
            self.dicreport_setup[self.production].update({'print': 'YES'})
            df.reset_index(inplace=True, drop=True)
            df.to_csv(pathfilename, index=False)
            print('\n Note: ' + pathfilename, ' has been writed with',
                  len(df), ' items \n')
        else:
            self.dicreport_setup[self.production].update({'print': 'NO'})
            print('------------------------------------------------------------\n' +
                  'ATTENTION \n' +
                  'There is NO ' + pathfilename + ' for this period.' + '\n' +
                  '------------------------------------------------------------')

    def column_year_running(self, df):
        """Filter year for running production e.g. advising running."""
        df['YEAR'] = [int(yy) for yy in df['YEAR'].to_list()]
        filename = self.dicreport_setup[self.production]['pathfilename'].split(
            '/')[-1]
        pathfilename = './relatorio/csv_report/' + 'report_' + filename
        if len(df) >= 1:
            self.dicreport_setup[self.production].update({'print': 'YES'})
            df.reset_index(inplace=True, drop=True)
            df.to_csv(pathfilename, index=False)
            print('\n Note: ' + pathfilename, ' has been writed with',
                  len(df), ' items \n')
        else:
            self.dicreport_setup[self.production].update({'print': 'NO'})
            print('------------------------------------------------------------\n' +
                  'ATTENTION \n' +
                  'There is NO ' + pathfilename + ' for this period.' + '\n' +
                  '------------------------------------------------------------')

    def column_year(self, df):
        """Filter production by means column year."""
        lsyear_limits = yearlimit_forfilter()
        df['YEAR'] = [int(yy) for yy in df['YEAR'].to_list()]
        df = df[(df['YEAR'] >= lsyear_limits[0]) &
                (df['YEAR'] <= lsyear_limits[1])]
        filename = self.dicreport_setup[self.production]['pathfilename'].split(
            '/')[-1]
        pathfilename = './relatorio/csv_report/' + 'report_' + filename
        if len(df) >= 1:
            self.dicreport_setup[self.production].update({'print': 'YES'})
            df.reset_index(inplace=True, drop=True)
            df.to_csv(pathfilename, index=False)
            print('\n Note: ' + pathfilename, ' has been writed with',
                  len(df), ' items \n')
        else:
            self.dicreport_setup[self.production].update({'print': 'NO'})
            print('------------------------------------------------------------\n' +
                  'ATTENTION \n' +
                  'There is NO ' + pathfilename + ' for this period.' + '\n' +
                  '------------------------------------------------------------')

    def column_indexh(self, df):
        """Tidy file from index H data."""
        filename = self.dicreport_setup[self.production]['pathfilename'].split(
            '/')[-1]
        pathfilename = './csv_producao_hindex/' + filename
        print('\n Note: ' + pathfilename, ' has been writed with',
              len(df), ' items \n')

    def column_graphonoint(self, df):
        """Tidy file for grapho with no interacions."""
        filename = self.dicreport_setup[self.production]['pathfilename'].split(
            '/')[-1]
        pathfilename = './relatorio/csv_report/' + 'report_' + filename
        if len(df) >= 1:
            self.dicreport_setup[self.production].update({'print': 'YES'})
            df.reset_index(inplace=True, drop=True)
            df.to_csv(pathfilename, index=False)
            print('\n Note: ' + pathfilename, ' has been writed with',
                  len(df), ' items \n')
        else:
            self.dicreport_setup[self.production].update({'print': 'NO'})

    def return_func(self, df):
        """Return the desired function."""
        func_toreturn = self.dicreport_setup[self.production]['func']
        return getattr(self, func_toreturn)(df)
