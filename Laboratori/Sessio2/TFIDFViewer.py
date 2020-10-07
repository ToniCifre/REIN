"""
.. module:: TFIDFViewer

TFIDFViewer
******

:Description: TFIDFViewer

    Receives two paths of files to compare (the paths have to be the ones used when indexing the files)

:Version: 

:Date:  05/06/2020
"""

from __future__ import print_function, division

import math

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

import argparse

import numpy as np


def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param client:
    :param index:
    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError('File [%s] not found' % path)
    else:
        return lfiles[0].meta.id


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics as two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_tf = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_tf[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_tf.items()), sorted(file_df.items())


def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param client:
    :param index:
    :param file_id:
    :return:
    """

    # Get document terms frequency and overall terms document frequency
    file_tf, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tf])
    dcount = doc_count(client, index)

    tfidfw = []
    for (t, w), (_, df) in zip(file_tf, file_df):
        tfidfw.append((t, (w / max_freq) * math.log2(dcount / df)))
    print(tfidfw)
    return normalize(tfidfw)


def normalize(tw):
    """
    Normalizes the weights in tw so that they form a unit-length vector
    It is assumed that not all weights are 0
    
    :param tw:
    :return:
    """
    norm = np.sqrt(np.sum([np.power(row, 2) for _, row in tw]))

    return [(term, tfidf / norm) for term, tfidf in tw]


def print_term_weight_vector(twv):
    """
    Prints the term vector and the corresponding weights
    
    :param twv:
    :return:
    """
    print(twv)


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    
    :param tw1:
    :param tw2:
    :return:
    """
    return np.sum(intersect(tw1, tw2))
    # simil = 0
    # for t, w in tw1:
    #     if t not in [t for t, _ in tw2]:
    #         print('polla')
    #         tw2.append((t, 0))
    # for t, w in tw2:
    #     if t not in [t for t, _ in tw1]:
    #         tw1.append((t, 0))
    # tw1 = sorted(tw1, key=lambda x: x[0])
    # tw2 = sorted(tw2, key=lambda x: x[0])
    # print(tw1)
    # print(tw2)
    # for (_, w1), (_, w2) in zip(tw1, tw2):
    #     simil += w1 * w2
    # return simil


def intersect(l1, l2):
    pos1 = 0
    pos2 = 0
    aux = []
    while len(l1) > pos1 and len(l2) > pos2:
        if l1[pos1][0] < l2[pos2][0]:
            pos1 += 1
        elif l1[pos1][0] > l2[pos2][0]:
            pos2 += 1
        else:
            aux.append(l1[pos1][1] * l2[pos2][1])
            pos1 += 1
            pos2 += 1
    return aux


def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default='proba', required=False, help='Index to search')
    parser.add_argument('--files', default=['docs/d3.txt', 'docs/d4.txt'], required=False, nargs=2,
                        help='Paths of the files to compare')
    parser.add_argument('--print', default=True, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()

    index = args.index

    file1 = args.files[0]
    file2 = args.files[1]
    print(args.files)

    client = Elasticsearch()

    try:
        # Get the files ids
        file1_id = search_file_by_path(client, index, file1)
        file2_id = search_file_by_path(client, index, file2)

        # Compute the TF-IDF vectors
        file1_tw = toTFIDF(client, index, file1_id)
        file2_tw = toTFIDF(client, index, file2_id)

        if args.print:
            print(f'TFIDF FILE {file1}')
            print_term_weight_vector(file1_tw)
            print('---------------------')
            print(f'TFIDF FILE {file2}')
            print_term_weight_vector(file2_tw)
            print('---------------------')

        print(f"Similarity = {cosine_similarity(file1_tw, file2_tw):3.5f}")

    except NotFoundError:
        print(f'Index {index} does not exist')
