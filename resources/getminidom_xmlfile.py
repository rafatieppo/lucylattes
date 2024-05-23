"""Get minidom from xml file."""

from xml.dom import minidom


def getminidom_xmlfile(xmlfile):
    """Get minidom from xml file."""
    minidomdoc = minidom.parse(xmlfile)
    # encoding = [xmldoc.encoding, xmldoc.version]
    print('A minidom has been createad.')
    return minidomdoc
