"""Get works inevent from xml file."""

import numpy as np
import pandas as pd
from resources.paper_qualis import paperqualis
from resources.paper_jcr import paperjcr


def getworksevents(zipname, minidomdoc):
    """Get works in envent from xml file."""
    # get full name to check author order
    id_lattes = str(zipname.split('.')[0])
    full_name = minidomdoc.getElementsByTagName('DADOS-GERAIS')[0] \
        .getAttributeNode('NOME-COMPLETO').nodeValue
    # search for producao-blibliografica starts here
    chd_prodbibliog = minidomdoc.getElementsByTagName('PRODUCAO-BIBLIOGRAFICA')
    if chd_prodbibliog.length > 0:
        # len_chd_prodbibliog = len(chd_prodbibliog[0].childNodes)
        # child producao bibliografica -> TRABALHOS-EM-EVENTOS
        chd_worksevents = chd_prodbibliog[0] \
            .getElementsByTagName('TRABALHOS-EM-EVENTOS')
        try:
            len_chd_worksevents = len(chd_worksevents[0].childNodes)
        # print('------------>>>> ', len_chd_worksevents)
            if len_chd_worksevents >= 1:
                ls_workevnt_nature = []
                ls_workevnt_title = []
                ls_workevnt_year = []
                # vls_per_doi = []
                # vls_per_lang = []
                # vls_per_journal = []
                # vls_per_issn = []
                # ls_per_qualis = []
                ls_per_authors = []
                ls_per_authorsorder = []
                ls_per_order = []
                ls_per_idcnpq = []
                # ls_jcr = []
                for idx in range(len_chd_worksevents):
                    workevnt_nature = chd_worksevents[0].childNodes[idx] \
                        .getElementsByTagName('DADOS-BASICOS-DO-TRABALHO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_worksevents[0].childNodes[idx] \
                        .getElementsByTagName('DADOS-BASICOS-DO-TRABALHO')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    year = chd_worksevents[0].childNodes[idx] \
                        .getElementsByTagName('DADOS-BASICOS-DO-TRABALHO')[0] \
                        .getAttributeNode('ANO-DO-TRABALHO').nodeValue
                    # doi = chd_worksevents[0].childNodes[idx] \
                    #     .getElementsByTagName('DADOS-BASICOS-DO-ARTIGO')[0] \
                    #     .getAttributeNode('DOI').nodeValue
                    # lang = chd_worksevents[0].childNodes[idx] \
                    #     .getElementsByTagName('DADOS-BASICOS-DO-ARTIGO')[0] \
                    #     .getAttributeNode('IDIOMA').nodeValue
                    # journal = chd_worksevents[0].childNodes[idx] \
                    #     .getElementsByTagName('DETALHAMENTO-DO-ARTIGO')[0] \
                    #     .getAttributeNode('TITULO-DO-PERIODICO-OU-REVISTA').nodeValue
                    # issn = chd_worksevents[0].childNodes[idx] \
                    #     .getElementsByTagName('DETALHAMENTO-DO-ARTIGO')[0] \
                    #     .getAttributeNode('ISSN').nodeValue

                    # child producao bibliografica -> artigos-publicados -> autores
                    ls_allauthors = []
                    ls_allauthororder = []
                    ls_authororder = []
                    ls_allidcnpq = []
                    chd_autores = chd_worksevents[0].childNodes[idx] \
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
                    ls_workevnt_nature.append(workevnt_nature)
                    ls_workevnt_title.append(title)
                    ls_workevnt_year.append(year)
                    # ls_per_doi.append(doi)
                    # ls_per_lang.append(lang)
                    # ls_per_journal.append(journal)
                    # ls_per_issn.append(issn)
                    # ls_per_qualis = []
                    ls_per_authors.append(ls_allauthors)
                    ls_per_authorsorder.append(ls_allauthororder)
                    ls_per_order.append(ls_authororder)
                    ls_per_idcnpq.append(ls_allidcnpq)
                    # ls_jcr = []

                # clean ls_per_order - remove brackets and to int
                # ls_per_order_clean = [int(xx[0]) for xx in ls_per_order]
                # print(ls_per_order)
                # to fix a minor issue - after to improve it
                ls_per_order_clean = []
                for xx in ls_per_order:
                    if len(xx) < 1:
                        rr = 99
                    else:
                        rr = int(xx[0])
                    ls_per_order_clean.append(rr)

                # set qualis and jcr
                # ls_per_qualis = paperqualis(ls_per_issn, qf)
                # ls_per_jcr = paperjcr(ls_per_issn)

                # write file
                df_workevnt = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                            len(ls_workevnt_title)),
                                            'NATURE': ls_workevnt_nature,
                                            'TITLE': ls_workevnt_title,
                                            'YEAR': ls_workevnt_year,
                                            # 'DOI': ls_per_doi,
                                            # 'LANG': ls_per_lang,
                                            # 'JOURNAL': ls_per_journal,
                                            # 'ISSN': ls_per_issn,
                                            # 'QUALIS': ls_per_qualis,
                                            # 'JCR': ls_per_jcr,
                                            'AUTHOR': ls_per_authors,
                                            'ORDER': ls_per_authorsorder,
                                            'ORDER_OK': ls_per_order_clean,
                                            'ID_CNPQ': ls_per_idcnpq
                                            })
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_worksevents.csv')
                df_workevnt.to_csv(pathfilename, index=False)
                print('The file ', pathfilename, ' has been writed.')
        except:
            print('The id Lattes ', id_lattes, ' has NO TRABALHOS-EM-EVENTOS')
    else:
        print('The id Lattes ', id_lattes, ' has NO PRODUCAO-BIBLIOGRAFICA.')
