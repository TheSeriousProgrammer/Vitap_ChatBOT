#!/usr/bin/python3

#================importing system modules========================
from rasa_nlu.model import Interpreter
import json
from fuzzywuzzy import process
from pprint import pprint
#================================================================

#================importing local library=========================
from ws_engine import initialize as initialize_ws
from ws_engine import searchWebsite
#================================================================

#================Initializing Program============================
nlp_interpreter = Interpreter.load("./models/current/nlu")
records = [x.split(",") for x in open("Book2.csv",'r').read().split("\n") ]
cleaned_records = [{"name":x[2]+x[3],"position":x[5],"department":x[6],"room":x[7],"block":x[8],"inter_number":x[9]} for x in records if len(x)==10]
names = [x["name"] for x in cleaned_records]

if __name__=="__main__":
    if( "y" in str(input("Shall I re-initialize spell corrector:"))):
        initialize_ws()
#================================================================

#================Main============================================
nlp_strings={
        "personQuery":"who is %s",
        "personContact":"contact %s",
        "objectQuery":"what is %s"
        }

def returnConsernedRecord(inp_str):
    global names

    matching_names = (process.extractBests(inp_str,names,limit=5,score_cutoff=70))
    pprint(matching_names)

    if matching_names ==[] :
        return None
    elif matching_names[0][1]>=95 or len(matching_names)==1 :
        return cleaned_records[names.index(matching_names[0][0])]
    else :
        return [x[0] for x in matching_names]

def handleNLPQuery(inp_str):
    global nlp_strings
    global nlp_interpreter

    response_nlp = nlp_interpreter.parse(inp_str)
    pprint(response_nlp)
    if(response_nlp['intent']['name']==None): #Checks if the query isnt understood and target isnt detected
        target =  inp_str #if so the whole query is converted to target
        #detection = False
    elif response_nlp['intent']['name']=="objectQuery" :
        return handleNLPQuery(response_nlp['entities'][0]['value'])
    elif response_nlp['intent']['name']=="courseQuery":
        if response_nlp['entities']==[]:
            return {
                    "mode":0,
                    "body":[["Click to see Programs Offered","https://vitap.ac.in/programmes-offered/"]]

            }
        else:
            target = response_nlp['entities'][0]['value']
            #detection=True
    else:
        target = response_nlp['entities'][0]['value']
        #detection = True

    records = returnConsernedRecord(target)

    if records == None :
        ws_result = searchWebsite(target)
        if ws_result == None :
            return {
                        "mode":-1
                   }
        else:
            return {
                        "mode":0,
                        "body":ws_result
                   }

    elif type(records)==type(dict()):

        if response_nlp['intent']['name']=="personContact" :

            return {
                        "mode":1,
                        "body":[    "Here is Some Information , which can help you",
                                    "Cabin Location  :%s"%(records['room']+","+records["block"]),
                                    "Telecom Number :%s"%(records['inter_number'])
                               ]
                   }

        else :
             return  {
                        "mode":1,
                        "body":[
                                    "Here is some information which might help you",
                                    "Name          : %s"%(records['name']),
                                    "Position Held : %s,"%(records['position']),
                                    "Department    : %s"%(records['department'])
                               ]
                    }





    else :
        body = []
        for i in records :
            if response_nlp['intent']['name']==None:
                body.append({"text":i,"value":"who is %s"%i})
            else:
                body.append({"text":i,"value":(nlp_strings[response_nlp["intent"]["name"]])%i})

        return {
                    "mode":2,
                    "body":body
               }


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

    while True :
        print("\n")
        message = str(input("Enter your test query:"))
        result = handleNLPQuery(message)
        pprint(result)
