#!/usr/bin/python3


from rasa_nlu.model import Interpreter
from json import dumps

nlp_interpreter = Interpreter.load("./models/current/nlu")

while True :
    inpQuery = str(input("Enter your query:"))
    response_nlp = nlp_interpreter.parse(inpQuery)
    print("\n\n")
    print(dumps(response_nlp,indent =4))
