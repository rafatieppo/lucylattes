"""Functions to clean titles and drop similar titles by means cosine similarity."""

import re
import pandas as pd
import numpy as np
import nltk
import string
from sklearn.feature_extraction.text import CountVectorizer
import math
from nltk.cluster.util import cosine_distance
import scipy
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_titles(dfdata, col_var):
    """
    Return a list. Pass to lower case, remove portuguese stops words and \
    punctuation.

    Keyword arguments:
    dfdata is a pandas data frame with productions.
    col_var is a string with the productions's column name
    """
    #  creating a list with titles
    lstitles = dfdata[col_var].to_list()
    # pass to lower case
    lslower = [text.lower() for text in lstitles]
    # clean stop words and punctuation
    stopwords = nltk.corpus.stopwords.words('portuguese')
    lstitles_clean = []
    for idx in range(len(lstitles)):
        text = lslower[idx]
        lstitle_nosw = [
            palavra for palavra in text.split(' ') if palavra not in stopwords]
        rgex = re.compile('[%s]' % re.escape(string.punctuation))
        text_clean = re.sub(rgex, '', ' '.join(lstitle_nosw))
        lstitles_clean.append(text_clean)
    return lstitles_clean


def drop_similar_rows(df, column, threshold):
    """
    Define a function to drop similar rows based on cosine similarity threshold.
    """
    lstitles_clean = clean_titles(df, column)
    dfdata = (
        df
        .assign(ID_X=np.arange(0, len(df)))
        .assign(TEXT_CLEAN=lstitles_clean)
        .sort_values(['ORDER_OK', 'YEAR'], axis=0)
        .reset_index(drop=True)
        )

    # Convert the text data to TF-IDF features
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(dfdata['TEXT_CLEAN'])
    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix)
    # Track rows to drop
    to_drop = set()
    for i in range(len(cosine_sim)):
        for j in range(i + 1, len(cosine_sim)):
            # If similarity is above threshold, mark for dropping
            if cosine_sim[i, j] > threshold:
                to_drop.add(j)
    # Drop rows with high similarity
    dfdata = dfdata.drop(list(to_drop)).reset_index(drop=True)
    return dfdata


def get_uniq_titles(dfdata, col_var, n, m, cosine_threshold):
    """
    Return a pandas data frame. Drop similar titles by means cosine similarity.

    Keyword arguments:
    dfdata is a pandas data frame with productions.
    col_var is a string with the productions's column name.
    cosine_threshold is the cosine threshold.
    n and m are the range (min_n, max_n) for n_gramas Bigrama.
    """
    # add newl cols in dfdata, sort values to keep first author
    lstitles_clean = clean_titles(dfdata, col_var)
    dfdata = (
        dfdata
        .assign(ID_X=np.arange(0, len(dfdata)))
        .assign(TEXT_CLEAN=lstitles_clean)
        .sort_values(['ORDER_OK', 'YEAR'], axis=0)
        )
    dfdata_uniq = dfdata.copy()

    counter = 0
    while counter < len(dfdata_uniq):
        lsindex_rm = []
        lscosine = []
        text_a = dfdata_uniq[col_var].iloc[counter]
        # print(dfdata_uniq[col_var].iloc[counter])
        for idy in range(len(dfdata_uniq)):
            if dfdata_uniq['ID_X'].iloc[counter] != dfdata_uniq['ID_X'].iloc[idy]:
                text_b = dfdata_uniq[col_var].iloc[idy]
                # instancia o contador de n-gramas
                counts = CountVectorizer(analyzer='word', ngram_range=(n, m))
                vocab = counts.fit([text_a, text_b])
                # check if tokens are in both or neither titles
                check = counts.fit_transform([text_a, text_b])
                check_arr = check.toarray()
                # cosine_distance
                cosine_dist = 1 - scipy.spatial.distance.cosine(
                    check_arr[0], check_arr[1])
                if cosine_dist > cosine_threshold:
                    lscosine.append(cosine_dist)
                    lsindex_rm.append(idy)
        counter += 1
        # removing index
        if len(lsindex_rm) > 0:
            print('Unique, removing: {}'.format(dfdata_uniq['TITLE'].iloc[counter]))
            # print('Comprimento lsindex_rm: {}'.format(len(lsindex_rm)))
            print('Index to remove: {}'.format(lsindex_rm))
            index_to_rm = set(range(dfdata_uniq.shape[0])) - set(lsindex_rm)
            dfdata_uniq = dfdata_uniq.take(list(index_to_rm))
            dfdata_uniq = dfdata_uniq.reset_index(drop=True)
            lsindex_rm = []
            lscosine = []
            # dfdata_uniq = dfdata_uniq.drop(dfdata_uniq.index([lsindex_rm]))
    dfdata_uniq.sort_values(['ID', 'YEAR'], inplace=True)
    dfdata_uniq.reset_index(inplace=True, drop=True)
    return dfdata_uniq
