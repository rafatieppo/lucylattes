"""Open and extract idlattes.zip from xml_zip folder."""

import zipfile


def unzip_xml(zipname):
    """Open and extract idlattes.zip from xml_zip folder."""
    # zipname = '3275865819287843.zip'
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    try:
        xmlFile = archive.open('curriculo.xml')
        print('A xml file from ', zipname, ' has been created.')
    except KeyError:
        xmlFile = archive.open(zipname.split('.')[0] + '.xml')
        print('A xml file from ', zipname, ' has been created.')
    return xmlFile
