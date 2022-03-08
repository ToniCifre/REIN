"""
.. module:: SearchIndex

SearchIndex
*************

:Description: SearchIndex

    Searches for a specific word in the field 'text' (--text)  or performs a query (--query) (LUCENE syntax,
    between single quotes) in the documents of an index (--index)
    

:Version: 

:Created on: 04/07/2020 

"""
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q


def search_mejortorrent():
    try:
        print('=== Mejor Torrent ===\n')

        s = Search(using=client, index='scrapy')

        q = Q('query_string', query=query)
        s = s.query(q)
        response = s[0:10].execute()

        for r in response:
            print(f'\n----- {r["Titulo"]} -------------------------')
            print(f'Género: {r["Género"]}')
            print(f'Actores: {r["Actores"]}')
            print(f'Formato: {r["Formato"]}')
            print(f'Tamaño:\n {r["Tamaño"]}')
            print(f'Descripción:\n {r["Descripción"]}')
            print(f'Link Descarga = {r["download"]}')
            print('=================================================')

        print('%d Documents' % response.hits.total.value)
    except NotFoundError:
        print('Index %s does not exist' % index)


def search_sensacine():
    try:
        print('=== SensaCine ===\n')

        s = Search(using=client, index='scrapy-sensacine')

        q = Q('query_string', query=query)
        s = s.query(q)
        response = s[0:10].execute()

        for r in response:
            print(f'\n----- {r["Titulo"]} -------------------------')
            print(f'Género: {r["Género"]}')
            print(f'Director: {r["Director"]}')
            print(f'Reparto: {r["Reparto"]}')
            print(f'Puntuación: {r["SensaCine"]} / {r["Medios"]} '
                  f'/ {r["Usuarios"]}')
            print(f'Sinopsis:\n {r["Sinopsis"]}')
            print('=================================================')

        print('%d Documents' % response.hits.total.value)
    except NotFoundError:
        print('Index %s does not exist' % index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search (scrapy-sensacine, scrapy, all)')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='Lucene query')

    args = parser.parse_args()

    index = args.index
    query = ' '
    if args.query:
        query = query.join(args.query)

    client = Elasticsearch()

    if index == 'scrapy-sensacine':
        search_sensacine()
    elif index == 'scrapy':
        search_mejortorrent()
    else:
        print('Index %s does not exist' % index)

