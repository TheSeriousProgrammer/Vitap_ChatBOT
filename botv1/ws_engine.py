#!/usr/bin/python3

from elasticsearch import Elasticsearch
#from elasticsearch_dsl import Search
from spellchecker import SpellChecker
from requests import get
from os import listdir
from pprint import pprint
from termcolor import cprint

PATH = "../Scraped_files"

es = Elasticsearch("---elasticsearch link here-----")

spellCorrector = SpellChecker(local_dictionary=(PATH+"/word_corpus"))

def initialize():
    global spellCorrector , es
    spellCorrector = SpellChecker(local_dictionary=(PATH+"/word_corpus"))
    es.indices.delete(index="vit-chatbot")
    es.indices.create(index="vit-chatbot")
    files=sorted(listdir(PATH))
    for i in files :
        if 'word' not in i :
            es.index(index='vit-chatbot',id=(int(i)+1),body=eval(open(PATH+"/"+i,'r').read()))

    print("Indexes Updated")

def changePath(inp_str):
    global PATH
    PATH = inp_str

def cureQuery(inp_str): #corrects speeling mistakes in a query
    out = ""
    for i in inp_str.split(' '):
        out+=(spellCorrector.correction(i)+" ")
    print()
    cprint("Fixed sentence:"+out,"magenta")
    print()
    return out[:-1]

def process_dict(inp_dict):
    out=[]
    for i in inp_dict['hits']['hits']:
        out.append([i["_source"]['title'],i["_source"]["link"]])
    return(out)

def searchWebsite(inp_str,max_results=10):
    global es

    inp_str = cureQuery(inp_str)
    response = es.search(index='vit-chatbot',body={'from':0,'size':max_results,'query':{"match":{"title":inp_str}}})
    if (response['hits']['max_score'])==None :
        response = es.search(index='vit-chatbot',body={'from':0,'size':max_results,'query':{"match":{"content":inp_str}}})
        if response['hits']['max_score']==None :
            return None
    return process_dict(response)

if __name__=="__main__":
    initialize()
    while True:
        pprint(searchWebsite(str(input("Enter your query:")),max_results=1000),indent = 4)
