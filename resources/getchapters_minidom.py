"""Get chapters from xml file."""

import numpy as np
import pandas as pd


def getchapters(zipname, minidomdoc):
    """Get chapters from xml file."""
    # get full name to check author order
    id_lattes = str(zipname.split('.')[0])
    full_name = minidomdoc.getElementsByTagName('DADOS-GERAIS')[0] \
        .getAttributeNode('NOME-COMPLETO').nodeValue
    # search for producao-blibliografica starts here
    chd_bookschapters = minidomdoc.getElementsByTagName('LIVROS-E-CAPITULOS')
    len_chd_bookschapters = chd_bookschapters.length
    len_chd_bookschapters
    # child livros-e-capitulos -> capitulos-de-livros-publicados
    if len_chd_bookschapters >= 1:
        chd_chappub = chd_bookschapters[0] \
            .getElementsByTagName('CAPITULOS-DE-LIVROS-PUBLICADOS')
        if chd_chappub.length >= 1:
            len_chd_chappub = len(chd_chappub[0].childNodes)
            ls_chap_type = []
            ls_chap_title = []
            ls_chap_year = []
            ls_chap_doi = []
            ls_chap_lang = []
            ls_chap_book = []
            ls_chap_publisher = []
            ls_chap_isbn = []
            ls_chap_authors = []
            ls_chap_authorsorder = []
            ls_chap_order = []
            ls_chap_idcnpq = []
            for idx in range(len_chd_chappub):
                typee = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-CAPITULO')[0] \
                    .getAttributeNode('TIPO').nodeValue
                title = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-CAPITULO')[0] \
                    .getAttributeNode('TITULO-DO-CAPITULO-DO-LIVRO').nodeValue
                year = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-CAPITULO')[0] \
                    .getAttributeNode('ANO').nodeValue
                doi = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-CAPITULO')[0] \
                    .getAttributeNode('DOI').nodeValue
                lang = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-CAPITULO')[0] \
                    .getAttributeNode('IDIOMA').nodeValue
                book = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DETALHAMENTO-DO-CAPITULO')[0] \
                    .getAttributeNode('TITULO-DO-LIVRO').nodeValue
                publisher = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DETALHAMENTO-DO-CAPITULO')[0] \
                    .getAttributeNode('NOME-DA-EDITORA').nodeValue
                isbn = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('DETALHAMENTO-DO-CAPITULO')[0] \
                    .getAttributeNode('ISBN').nodeValue
                # child producao bibliografica -> artigos-publicados -> autores
                ls_allauthors = []
                ls_allauthororder = []
                ls_authororder = []
                ls_allidcnpq = []
                chd_autores = chd_chappub[0].childNodes[idx] \
                    .getElementsByTagName('AUTORES')
                len_chd_autores = chd_autores.length
                for idy in range(len_chd_autores):
                    author = chd_autores[idy] \
                        .getAttributeNode('NOME-COMPLETO-DO-AUTOR').nodeValue
                    authors_order = chd_autores[idy] \
                        .getAttributeNode('ORDEM-DE-AUTORIA').nodeValue
                    idcnpq = chd_autores[idy] \
                        .getAttributeNode('NRO-ID-CNPQ').nodeValue
                    ls_allauthors.append(author)
                    ls_allauthororder.append(authors_order)
                    ls_allidcnpq.append(idcnpq)
                    # assign author order
                    if author == full_name:
                        ls_authororder.append(authors_order)
                ls_chap_type.append(typee)
                ls_chap_title.append(title)
                ls_chap_year.append(year)
                ls_chap_doi.append(doi)
                ls_chap_lang.append(lang)
                ls_chap_book.append(book)
                ls_chap_publisher.append(publisher)
                ls_chap_isbn.append(isbn)
                ls_chap_authors.append(ls_allauthors)
                ls_chap_authorsorder.append(ls_allauthororder)
                ls_chap_order.append(ls_authororder)
                ls_chap_idcnpq.append(ls_allidcnpq)
            # clean ls_per_order - remove brackets and to int
            # ls_chap_order_clean = [int(xx[0]) for xx in ls_chap_order]
            # to fix a minor issue - after to improve it - same in getpaper
            ls_chap_order_clean = []
            for xx in ls_chap_order:
                if len(xx) < 1:
                    rr = 99
                else:
                    rr = int(xx[0])
                ls_chap_order_clean.append(rr)
            df_chapters = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                        len(ls_chap_title)),
                                        'TITLE': ls_chap_title,
                                        'TYPE': ls_chap_type,
                                        'YEAR': ls_chap_year,
                                        'DOI': ls_chap_doi,
                                        'LANG': ls_chap_lang,
                                        'BOOK': ls_chap_book,
                                        'PUBLISHER': ls_chap_publisher,
                                        # 'QUALIS': ls_chap_qualis,
                                        'ISSN': ls_chap_isbn,
                                        'AUTHOR': ls_chap_authors,
                                        'ORDER': ls_chap_authorsorder,
                                        'ORDER_OK': ls_chap_order_clean,
                                        'ID_CNPQ': ls_chap_idcnpq
                                        # 'JCR': ls_jcr
                                        })
            pathfilename = str('./csv_producao/' +
                               id_lattes + '_chapters.csv')
            df_chapters.to_csv(pathfilename, index=False)
            print('The file ', pathfilename, ' has been writed.')
        else:
            print('The id Lattes ', id_lattes,
                  ' has NO  CAPITULOS-DE-LIVROS-PUBLICADOS.')
    else:
        print('The id Lattes ', id_lattes, ' has NO LIVROS-E-CAPITULOS.')
