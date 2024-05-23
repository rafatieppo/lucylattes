"""Get advising from xml file."""

import numpy as np
import pandas as pd


def getadv(zipname, minidomdoc):
    """Get advising from xml file."""
    id_lattes = str(zipname.split('.')[0])
    # search for outra-producao starts here
    chd_otherprod = minidomdoc.getElementsByTagName('OUTRA-PRODUCAO')
    len_chd_otherprod = chd_otherprod.length
    len_chd_otherprod

    # child outra-producao -> orientacoes-concluidas
    if len_chd_otherprod >= 1:
        chd_advfinish = chd_otherprod[0] \
            .getElementsByTagName('ORIENTACOES-CONCLUIDAS')
        if chd_advfinish.length >= 1:
            ls_adv_year = []
            ls_adv_nat = []
            ls_adv_title = []
            ls_adv_inst = []
            ls_adv_course = []
            ls_adv_courseid = []
            ls_adv_pupil = []
            ls_adv_typeadv = []
            ls_adv_suppo = []
            ls_adv_idcnpq_pupil = []

            # child outra-producao -> orientacoes-concluidas -> ori-conc-p-mestrad
            chd_advmaster = chd_advfinish[0] \
                .getElementsByTagName(
                'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')
            len_chd_advmaster = chd_advmaster.length
            len_chd_advmaster
            if len_chd_advmaster >= 1:
                for idx in range(len_chd_advmaster):
                    year = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('TITULO').nodeValue
                    instit = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('NOME-DA-INSTITUICAO').nodeValue
                    course = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('NOME-DO-CURSO').nodeValue
                    courseid = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTADO').nodeValue
                    typeadv = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTADO').nodeValue
                    ls_adv_year.append(year)
                    ls_adv_nat.append(nature)
                    ls_adv_title.append(title)
                    ls_adv_inst.append(instit)
                    ls_adv_course.append(course)
                    ls_adv_courseid.append(courseid)
                    ls_adv_pupil.append(pupil)
                    ls_adv_typeadv.append(typeadv)
                    ls_adv_suppo.append(support)
                    ls_adv_idcnpq_pupil.append(pupil_idcnpq)
            else:
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_advis.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACOES-CONCLUIDAS-PARA-MESTRADO.')

            # child outra-producao -> orientacoes-concluidas -> ori-conc-p-doutorado
            chd_advdoc = chd_advfinish[0] \
                .getElementsByTagName(
                'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')
            len_chd_advdoc = chd_advdoc.length
            len_chd_advdoc
            if len_chd_advdoc >= 1:
                for idx in range(len_chd_advdoc):
                    year = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('TITULO').nodeValue
                    instit = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DA-INSTITUICAO').nodeValue
                    course = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-CURSO').nodeValue
                    courseid = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTADO').nodeValue
                    typeadv = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTADO').nodeValue
                    ls_adv_year.append(year)
                    ls_adv_nat.append(nature)
                    ls_adv_title.append(title)
                    ls_adv_inst.append(instit)
                    ls_adv_course.append(course)
                    ls_adv_courseid.append(courseid)
                    ls_adv_pupil.append(pupil)
                    ls_adv_typeadv.append(typeadv)
                    ls_adv_suppo.append(support)
                    ls_adv_idcnpq_pupil.append(pupil_idcnpq)
            else:
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_advis.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO.')

            # child outra-producao -> orientacoes-concluidas -> ori-conc-p-posdoc
            chd_advposdoc = chd_advfinish[0] \
                .getElementsByTagName(
                'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')
            len_chd_advposdoc = chd_advposdoc.length
            len_chd_advposdoc
            if len_chd_advposdoc >= 1:
                for idx in range(len_chd_advposdoc):
                    year = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO')[0] \
                        .getAttributeNode('TITULO').nodeValue
                    instit = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DA-INSTITUICAO').nodeValue
                    course = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-CURSO').nodeValue
                    courseid = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTADO').nodeValue
                    typeadv = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTADO').nodeValue
                    ls_adv_year.append(year)
                    ls_adv_nat.append(nature)
                    ls_adv_title.append(title)
                    ls_adv_inst.append(instit)
                    ls_adv_course.append(course)
                    ls_adv_courseid.append(courseid)
                    ls_adv_pupil.append(pupil)
                    ls_adv_typeadv.append(typeadv)
                    ls_adv_suppo.append(support)
                    ls_adv_idcnpq_pupil.append(pupil_idcnpq)
            else:
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_advis.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO.')

            # child outra-producao -> orientacoes-concluidas -> outras-orien-conc
            chd_advothers = chd_advfinish[0] \
                .getElementsByTagName(
                'OUTRAS-ORIENTACOES-CONCLUIDAS')
            len_chd_advothers = chd_advothers.length
            len_chd_advothers
            if len_chd_advothers >= 1:
                for idx in range(len_chd_advothers):
                    year = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('TITULO').nodeValue
                    instit = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('NOME-DA-INSTITUICAO').nodeValue
                    course = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('NOME-DO-CURSO').nodeValue
                    courseid = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('NOME-DO-ORIENTADO').nodeValue
                    typeadv = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO-CONCLUIDA').nodeValue
                    support = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTADO').nodeValue
                    ls_adv_year.append(year)
                    ls_adv_nat.append(nature)
                    ls_adv_title.append(title)
                    ls_adv_inst.append(instit)
                    ls_adv_course.append(course)
                    ls_adv_courseid.append(courseid)
                    ls_adv_pupil.append(pupil)
                    ls_adv_typeadv.append(typeadv)
                    ls_adv_suppo.append(support)
                    ls_adv_idcnpq_pupil.append(pupil_idcnpq)
            else:
                pathfilename = str('./csv_producao/' +
                                   id_lattes + '_advis.csv')
                print('The file ',
                      pathfilename,
                      ' has NO OUTRAS-ORIENTACOES-CONCLUIDAS.')
            df_advis = pd.DataFrame({'ID': np.repeat(id_lattes,
                                                     len(ls_adv_title)),
                                     'TITLE': ls_adv_title,
                                     'YEAR': ls_adv_year,
                                     'NATURE': ls_adv_nat,
                                     'INSTITUTION': ls_adv_inst,
                                     'COURSE': ls_adv_course,
                                     'COURSE_ID': ls_adv_courseid,
                                     'PUPIL': ls_adv_pupil,
                                     'PUPIL_IDCNPQ': ls_adv_idcnpq_pupil,
                                     'TYPE_ADV': ls_adv_typeadv,
                                     'SPONSOR': ls_adv_suppo})
            pathfilename = str('./csv_producao/' + id_lattes + '_advis.csv')
            df_advis.to_csv(pathfilename, index=False)
            print('The file ', pathfilename, ' has been writed.')
        else:
            print('The id Lattes ', id_lattes,
                  ' has NO ORIENTACOES-CONCLUIDAS.')
    else:
        print('The id Lattes ', id_lattes, ' has NO OUTRA-PRODUCAO.')
