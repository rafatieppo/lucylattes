"""Read names of files available in txt file and return a list."""


def read_jcr_qls(path_file):
    """
    Return a list with Read names of files available in a txt file.
    """
    with open(path_file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        f.close()
        return lines
