# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch

from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Index, analyzer, tokenizer
from elasticsearch.helpers import bulk


class ReinscrapyPipeline:
    def process_item(self, item, spider):
        return item


class MejorTorrentElasticPipeline(object):
    collection_name = 'scrapy-MejorTorrent'

    def __init__(self):
        self.client = Elasticsearch()
        self.elastic_uri = 'http://localhost:9200/'
        self.elastic_db = 'scrapy-mejortorrent'

        self.l_docs = []
        self.n_docs = 500
        self.index_dic = {'_op_type': 'index', '_index': self.elastic_db, '_type': 'MejorTorrent'}

    def open_spider(self, spider):
        try:
            ind = Index(self.elastic_db, using=self.client)
            # Drop index if it exists
            ind.delete()
        except NotFoundError:
            pass
        # then create it
        ind.create()
        ind.close()
        # Configure tokenizer
        my_analyzer = analyzer('default', type='custom', tokenizer=tokenizer('standard'),
                               filter=['lowercase', 'asciifolding'])
        ind.analyzer(my_analyzer)
        ind.save()
        ind.open()

    def close_spider(self, spider):
        if len(self.l_docs) > 0:
            print('[INFO] Indexing ...', end='')

            bulk(self.client, self.l_docs)
            self.l_docs.clear()

            print('    [OK]')

        self.client.close()

    def process_item(self, item, spider):
        self.l_docs.append({**self.index_dic, **item})

        if len(self.l_docs) > self.n_docs:
            print('[INFO] Indexing ...', end='')

            bulk(self.client, self.l_docs)
            self.l_docs.clear()

            print('    [OK]')

        return item


class SensaCineElasticPipeline(object):
    collection_name = 'scrapy-sensacine'

    def __init__(self):
        self.client = Elasticsearch()
        self.elastic_uri = 'http://localhost:9200/'
        self.elastic_db = 'scrapy-sensacine'

        self.l_docs = []
        self.n_docs = 500
        self.index_dic = {'_op_type': 'index', '_index': self.elastic_db, '_type': 'SensaCine'}

    def open_spider(self, spider):
        try:
            ind = Index(self.elastic_db, using=self.client)
            # Drop index if it exists
            ind.delete()
        except NotFoundError:
            pass
        # then create it
        ind.create()
        ind.close()
        # Configure tokenizer
        my_analyzer = analyzer('default', type='custom', tokenizer=tokenizer('standard'),
                               filter=['lowercase', 'asciifolding'])
        ind.analyzer(my_analyzer)
        ind.save()
        ind.open()

    def close_spider(self, spider):
        if len(self.l_docs) > 0:
            print('[INFO] Indexing ...', end='')

            bulk(self.client, self.l_docs)
            self.l_docs.clear()

            print('    [OK]')
        self.client.close()

    def process_item(self, item, spider):
        self.l_docs.append({**self.index_dic, **item})

        if len(self.l_docs) > self.n_docs:
            print('[INFO] Indexing ...', end='')

            bulk(self.client, self.l_docs)
            self.l_docs.clear()

            print('    [OK]')

        return item
