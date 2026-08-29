"""Get books from xml file."""

import numpy as np
import pandas as pd


def getbooks(zipname, minidomdoc):
    """Get books from xml file."""
    # get full name to check author order
    id_lattes = str(zipname.split('.')[0])
    full_name = minidomdoc.getElementsByTagName('DADOS-GERAIS')[0] \
        .getAttributeNode('NOME-COMPLETO').nodeValue

    # search for producao-blibliografica starts here
    chd_bookschapters = minidomdoc.getElementsByTagName('LIVROS-E-CAPITULOS')
    len_chd_bookschapters = chd_bookschapters.length
    len_chd_bookschapters

    # child livros-e-capitulos -> livros-publicados-ou-organizados
    if len_chd_bookschapters >= 1:
        chd_bookspuborg = chd_bookschapters[0] \
            .getElementsByTagName('LIVROS-PUBLICADOS-OU-ORGANIZADOS')
        if chd_bookspuborg.length >= 1:
            len_chd_artspubs = len(chd_bookspuborg[0].childNodes)
            len_chd_artspubs
            ls_book_type = []
            ls_book_title = []
            ls_book_year = []
            ls_book_doi = []
            ls_book_lang = []
            ls_book_publisher = []
            ls_book_isbn = []
            ls_book_authors = []
            ls_book_authorsorder = []
            ls_book_order = []
            ls_book_idcnpq = []
            for idx in range(len_chd_artspubs):
                typee = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-LIVRO')[0] \
                    .getAttributeNode('TIPO').nodeValue
                title = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-LIVRO')[0] \
                    .getAttributeNode('TITULO-DO-LIVRO').nodeValue
                year = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-LIVRO')[0] \
                    .getAttributeNode('ANO').nodeValue
                doi = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-LIVRO')[0] \
                    .getAttributeNode('DOI').nodeValue
                lang = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DADOS-BASICOS-DO-LIVRO')[0] \
                    .getAttributeNode('IDIOMA').nodeValue
                publisher = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DETALHAMENTO-DO-LIVRO')[0] \
                    .getAttributeNode('NOME-DA-EDITORA').nodeValue
                isbn = chd_bookspuborg[0].childNodes[idx] \
                    .getElementsByTagName('DETALHAMENTO-DO-LIVRO')[0] \
                    .getAttributeNode('ISBN').nodeValue

                # child producao bibliografica -> artigos-publicados -> autores
                ls_allauthors = []
                ls_allauthororder = []
                ls_authororder = []
                ls_allidcnpq = []
                chd_autores = chd_bookspuborg[0].childNodes[idx] \
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
                ls_book_type.append(typee)
                ls_book_title.append(title)
                ls_book_year.append(year)
                ls_book_doi.append(doi)
                ls_book_lang.append(lang)
                ls_book_publisher.append(publisher)
                ls_book_isbn.append(isbn)
                ls_book_authors.append(ls_allauthors)
                ls_book_authorsorder.append(ls_allauthororder)
                ls_book_order.append(ls_authororder)
                ls_book_idcnpq.append(ls_allidcnpq)
            # clean ls_per_order - remove brackets and to int
            # ls_book_order_clean = [int(xx[0]) for xx in ls_book_order]
            # print(ls_book_order)
            # to fix a minor issue - after to improve it
            ls_book_order_clean = []
            for xx in ls_book_order:
                if len(xx) < 1:
                    rr = 99
                else:
                    rr = int(xx[0])
                ls_book_order_clean.append(rr)

            # write file
            df_books = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                     len(ls_book_title)),
                                     'TITLE': ls_book_title,
                                     'TYPE': ls_book_type,
                                     'YEAR': ls_book_year,
                                     'DOI': ls_book_doi,
                                     'LANG': ls_book_lang,
                                     'PUBLISHER': ls_book_publisher,
                                     # 'QUALIS': ls_book_qualis,
                                     'ISSN': ls_book_isbn,
                                     'AUTHOR': ls_book_authors,
                                     'ORDER': ls_book_authorsorder,
                                     'ORDER_OK': ls_book_order_clean,
                                     'ID_CNPQ': ls_book_idcnpq
                                     # 'JCR': ls_jcr
                                     })
            pathfilename = str('./csv_producao/' +
                               id_lattes + '_books.csv')
            df_books.to_csv(pathfilename, index=False)
            print('The file ', pathfilename, ' has been writed.')
        else:
            print('The id Lattes ', id_lattes,
                  ' has NO LIVROS-PUBLICADOS-OU-ORGANIZADOS.')
    else:
        print('The id Lattes ', id_lattes, ' has NO LIVROS-E-CAPITULOS.')
