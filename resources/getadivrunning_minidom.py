"""Get advising running from xml file."""

import numpy as np
import pandas as pd


def getadvrunn(zipname, minidomdoc):
    """Get advising running from xml file."""
    id_lattes = str(zipname.split('.')[0])
    # search for dados-complementares starts here
    chd_compdata = minidomdoc.getElementsByTagName('DADOS-COMPLEMENTARES')
    len_chd_compdata = chd_compdata.length
    len_chd_compdata

    # child dados-complementares -> orientacoes-em-andamento
    if len_chd_compdata >= 1:
        chd_advrunn = chd_compdata[0] \
            .getElementsByTagName('ORIENTACOES-EM-ANDAMENTO')
        if chd_advrunn.length >= 1:
            ls_adv_seq = []
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

            # child dados-complementares -> orientacoes-em-andamento -> ori-and-de-mestrad
            chd_advmaster = chd_advrunn[0] \
                .getElementsByTagName(
                'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')
            len_chd_advmaster = chd_advmaster.length
            len_chd_advmaster
            if len_chd_advmaster >= 1:
                for idx in range(len_chd_advmaster):
                    seq = chd_advmaster[idx] \
                        .getAttributeNode('SEQUENCIA-PRODUCAO').nodeValue
                    year = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    instit = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('NOME-INSTITUICAO').nodeValue
                    course = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('NOME-CURSO').nodeValue
                    courseid = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTANDO').nodeValue
                    typeadv = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advmaster[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTADO').nodeValue
                    ls_adv_seq.append(seq)
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
                                   id_lattes + '_advisrunn.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACOES-EM-ANDAMENTO-DE-MESTRADO.')

            # child dados-complementares -> orientacoes-em-andamento -> ori-and-de-dout
            chd_advdoc = chd_advrunn[0] \
                .getElementsByTagName(
                'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')
            len_chd_advdoc = chd_advdoc.length
            len_chd_advdoc
            if len_chd_advdoc >= 1:
                for idx in range(len_chd_advdoc):
                    seq = chd_advdoc[idx] \
                        .getAttributeNode('SEQUENCIA-PRODUCAO').nodeValue
                    year = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    instit = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('NOME-INSTITUICAO').nodeValue
                    course = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('NOME-CURSO').nodeValue
                    courseid = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTANDO').nodeValue
                    typeadv = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTANDO').nodeValue
                    ls_adv_seq.append(seq)
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
                                   id_lattes + '_advisrunn.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO.')

            # child dados-complementares -> orientacoes-em-andamento -> ori-and-de-pos-doc
            chd_advposdoc = chd_advrunn[0] \
                .getElementsByTagName(
                'ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')
            len_chd_advposdoc = chd_advposdoc.length
            if len_chd_advposdoc >= 1:
                for idx in range(len_chd_advposdoc):
                    seq = chd_advposdoc[idx] \
                        .getAttributeNode('SEQUENCIA-PRODUCAO').nodeValue
                    year = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    instit = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-INSTITUICAO').nodeValue
                    course = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-CURSO').nodeValue
                    courseid = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTANDO').nodeValue
                    typeadv = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advposdoc[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTANDO').nodeValue
                    ls_adv_seq.append(seq)
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
                                   id_lattes + '_advisrunn.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO.')

            # ------------------------------------------------------------
            # child dados-complementares -> orientacoes-em-andamento -> ic
            chd_advic = chd_advrunn[0] \
                .getElementsByTagName(
                'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')
            len_chd_advic = chd_advic.length
            if len_chd_advic >= 1:
                for idx in range(len_chd_advic):
                    seq = chd_advic[idx] \
                        .getAttributeNode('SEQUENCIA-PRODUCAO').nodeValue
                    year = chd_advic[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advic[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advic[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    instit = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('NOME-INSTITUICAO').nodeValue
                    course = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('NOME-CURSO').nodeValue
                    courseid = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('NOME-DO-ORIENTANDO').nodeValue
                    typeadv = str('')
                    # chd_advic[idx] \
                    #     .getElementsByTagName(
                    #     'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                    #     .getAttributeNode('TIPO-DE-ORIENTACAO').nodeValue
                    support = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advic[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTANDO').nodeValue
                    ls_adv_seq.append(seq)
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
                                   id_lattes + '_advisrunn.csv')
                print('The file ',
                      pathfilename,
                      ' has NO ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA.')

            # child dados-complementares -> orientacoes-em-andamento -> outras
            chd_advothers = chd_advrunn[0] \
                .getElementsByTagName(
                'OUTRAS-ORIENTACOES-EM-ANDAMENTO')
            len_chd_advothers = chd_advothers.length
            if len_chd_advothers >= 1:
                for idx in range(len_chd_advothers):
                    seq = chd_advothers[idx] \
                        .getAttributeNode('SEQUENCIA-PRODUCAO').nodeValue
                    year = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('ANO').nodeValue
                    nature = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('NATUREZA').nodeValue
                    title = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('TITULO-DO-TRABALHO').nodeValue
                    instit = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('NOME-INSTITUICAO').nodeValue
                    course = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('NOME-CURSO').nodeValue
                    courseid = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('CODIGO-CURSO').nodeValue
                    pupil = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('NOME-DO-ORIENTANDO').nodeValue
                    typeadv = str('')
                    # chd_advothers[idx] \
                    #     .getElementsByTagName(
                    #     'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                    #     .getAttributeNode('TIPO-DE-ORIENTACAO-CONCLUIDA').nodeValue
                    support = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('FLAG-BOLSA').nodeValue
                    pupil_idcnpq = chd_advothers[idx] \
                        .getElementsByTagName(
                        'DETALHAMENTO-DE-OUTRAS-ORIENTACOES-EM-ANDAMENTO')[0] \
                        .getAttributeNode('NUMERO-ID-ORIENTANDO').nodeValue
                    ls_adv_seq.append(seq)
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
                                   id_lattes + '_advisrunn.csv')
                print('The file ',
                      pathfilename,
                      ' has NO OUTRAS-ORIENTACOES-EM-ANDAMENTO.')
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
            pathfilename = str('./csv_producao/' +
                               id_lattes + '_advisrunn.csv')
            df_advis.to_csv(pathfilename, index=False)
            print('The file ', pathfilename, ' has been writed.')
        else:
            print('The id Lattes ', id_lattes,
                  ' has NO ORIENTACOES-EM-ANDAMENTO.')
    else:
        print('The id Lattes ', id_lattes, ' has NO ORIENTACOES-EM-ANDAMENTO.')
