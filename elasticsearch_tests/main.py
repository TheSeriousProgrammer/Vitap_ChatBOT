#!/usr/bin/python3

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from pprint import pprint

es = Elasticsearch('https://search-vitap-web-index-3ngpbsiwo3vl6e7qn75skx7dci.us-east-2.es.amazonaws.com/')

doc1 = {'content':"this world is beautiful , hello"}

doc2 = {"content":"first hello world program was created by james gosling"}

doc3 = {"conten":"The first world war was waged by the british on 21st hello"}

es.indices.create(index="tests")

es.index(index='tests',id=1,body=doc1)
es.index(index='tests',id=2,body=doc2)
es.index(index='tests',id=3,body=doc3)


s = Search(using=es , index="tests")\
        .filter("term",category="search")\
        .query("match",title='hello world')

resp = s.execute()


pprint(resp)
