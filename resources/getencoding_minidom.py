"""Get encoding and version from minidom."""

import pandas as pd


def getencoding_minidom(zipname, minidomdoc):
    """Get encoding and version from minidom."""
    encoding = [minidomdoc.encoding, minidomdoc.version]
    id_lattes = str(zipname.split('.')[0])
    df_encoding = pd.DataFrame({'ID': pd.Series(id_lattes),
                                'ENCODING': pd.Series(encoding[0]),
                                'VERSION': pd.Series(encoding[1])})
    pathfilename = str('./csv_producao/' + id_lattes + '_encoding.csv')
    df_encoding.to_csv(pathfilename, index=False)
    print('The file ', pathfilename, ' has been writed.')
    # return df_encoding
