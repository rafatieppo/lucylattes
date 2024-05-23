"""Get shor courses from xml file."""

import numpy as np
import pandas as pd


def getshortcourse(zipname, minidomdoc):
    """Get books from xml file."""
    id_lattes = str(zipname.split('.')[0])
    # search for producao-tecnica starts here
    chd_prodtec = minidomdoc.getElementsByTagName('PRODUCAO-TECNICA')
    len_chd_prodtec = chd_prodtec.length
    len_chd_prodtec
    # child producao-tecnica -> chd demais-tipos-de-producao-tecnica
    if len_chd_prodtec >= 1:
        chd_demaisprodtec = chd_prodtec[0] \
            .getElementsByTagName('DEMAIS-TIPOS-DE-PRODUCAO-TECNICA')

        # child producao-tec -> chd demais-tipos-de-produc-tec -> curs-d-curt-dur-m
        if chd_demaisprodtec.length >= 1:
            chd_cursocurtdur = chd_demaisprodtec[0] \
                .getElementsByTagName('CURSO-DE-CURTA-DURACAO-MINISTRADO')
            if chd_cursocurtdur.length >= 1:
                ls_scourse_title = []
                ls_scourse_year = []
                ls_scourse_authors = []
                ls_scourse_authors_idcnpq = []
                for idx in range(chd_cursocurtdur.length):
                    title = chd_cursocurtdur[idx] \
                        .getElementsByTagName(
                            'DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO')[0] \
                        .getAttributeNode('TITULO').nodeValue
                    year = chd_cursocurtdur[idx] \
                        .getElementsByTagName(
                            'DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    # authors
                    chd_autores = chd_cursocurtdur[idx] \
                        .getElementsByTagName('AUTORES')
                    ls_scourse_authors_temp = []
                    ls_scourse_authors_idcnpq_temp = []
                    for idy in range(chd_autores.length):
                        author = chd_autores[idy].getAttributeNode(
                            'NOME-COMPLETO-DO-AUTOR').nodeValue
                        autoridcnpq = chd_autores[idy].getAttributeNode(
                            'NRO-ID-CNPQ').nodeValue
                        ls_scourse_authors_temp.append(author)
                        ls_scourse_authors_idcnpq_temp.append(autoridcnpq)
                    ls_scourse_title.append(title)
                    ls_scourse_year.append(year)
                    ls_scourse_authors.append(ls_scourse_authors_temp)
                    ls_scourse_authors_idcnpq.append(
                        ls_scourse_authors_idcnpq_temp)

                df_shortcourse = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                               len(ls_scourse_title)),
                                               'COURSE': ls_scourse_title,
                                               'YEAR': ls_scourse_year,
                                               'AUTHOR': ls_scourse_authors,
                                               'ID_CNPQ': ls_scourse_authors_idcnpq
                                               })
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_shortcourse.csv')
                df_shortcourse.to_csv(pathfilename, index=False)
                print('The file ', pathfilename, ' has been writed.')
            else:
                print('The id Lattes ', id_lattes,
                      ' has NO CURSO-DE-CURTA-DURACAO-MINISTRADO.')
        else:
            print('The id Lattes ', id_lattes,
                  ' has NO DEMAIS-TIPOS-DE-PRODUCAO-TECNICA.')
    else:
        # pathfilename = str('./csv_producao/' + id_lattes + '_shortcourses.csv')
        print('The id Lattes ', id_lattes, ' has NO PRODUCAO-TECNICA.')
