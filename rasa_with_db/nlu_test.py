#!/usr/bin/python3

from rasa_nlu.model import Interpreter
import json
from fuzzywuzzy import process
from pprint import pprint

nlp_interpreter = Interpreter.load("./models/current/nlu")

records = [x.split(",") for x in open("Book2.csv",'r').read().split("\n") ]

cleaned_records = [{"name":x[2]+x[3],"position":x[5],"department":x[6],"room":x[7],"block":x[8],"inter_number":x[9]} for x in records if len(x)==10]

names = [x["name"] for x in cleaned_records]

def returnConsernedRecord(inp_str):
    global names

    matching_names = (process.extractBests(inp_str,names,limit=5,score_cutoff=55))
    pprint(matching_names)

    if matching_names ==[] :
        return None
    elif matching_names[0][1]>95 :
        return cleaned_records[names.index(matching_names[0][0])]
    else :
        return [x[0] for x in matching_names]

def handleNLPQuery(inp_str):
    global nlp_interpreter

    response_nlp = nlp_interpreter.parse(inp_str)
    #pprint(response)
    if(response_nlp['entities']==[]):
        target = inp_str
        detection = False
    else:
        target = response_nlp['entities'][0]['value']
        detection = True

    records = returnConsernedRecord(target)

    if records == None :
        return None

    elif type(records)==type(dict()):

        if not(detection) or response_nlp['intent']['name']=="personQuery" :
            return  {
                        "mode":1,
                        "body":[
                                    "Here is some information which might help you",
                                    "Name</b>     : %s"%(records['name']),
                                    "Postion Held : %s,"%(records['position']),
                                    "Department   : %s"%(records['department'])
                               ]
                    }

        elif response_nlp['intent']['name']=="personContact" :

            return {
                        "mode":1,
                        "body":[    "Here is Some Information , which can help you"
                                    "Cabin Location :%s"%(records['room']+" "+records["block"]),
                                    "Telecom Number :%s"%(records['inter_number'])
                               ]
                   }


    else :
        return {"mode":2,"body":["Multiple Similar Records Found",{"records":records,"intent":response_nlp["intent"]["name"]}]}


"""
Sample Response from nlp engine
{
  "intent": {
    "name": "personQuery",
    "confidence": 0.9257804751396179
  },
  "entities": [
    {
      "start": 7,
      "end": 18,
      "value": "aodihasjkda",
      "entity": "target",
      "confidence": 0.9978478650743986,
      "extractor": "CRFEntityExtractor"
    }
  ],
  "intent_ranking": [
    {
      "name": "personQuery",
      "confidence": 0.9257804751396179
    },
    {
      "name": "personContact",
      "confidence": 0.13004229962825775
    },
    {
      "name": "objectQuery",
      "confidence": 0.0
    }
  ],
  "text": "who is aodihasjkda"
}

"""
if __name__=="__main__":
    message = str(input("Enter your test query:"))
    result = handleNLPQuery(message)
    pprint(result)
