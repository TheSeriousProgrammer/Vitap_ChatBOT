#!/usr/bin/python3

from pprint import pprint
from os import path
from os import chdir
from json import dumps
chdir("/home/captain-america/Programming/BOT/botv1")

import tornado.web
import tornado.httpserver
from nlu_with_db_ws import handleNLPQuery
from json import dumps
from ws_engine import initialize as init_ws

from sys import argv

CONSOLE_MODE=False

if(len(argv)==1):
    print("Updating Spell Correction Indexes")
    init_ws()
    print("Done Updating Spell Correction Indexes")
elif (argv[1]=="console"):
    CONSOLE_MODE = True

class ChatbotServer(tornado.web.RequestHandler):
    def get(self):
        query=""
        try:
            query=self.get_argument("query")
            mode=self.get_argument("mode")
            if mode=="0":
                response = handleNLPQuery(query)
                if(response["mode"])==-1:
                    open("dontKnowWhatToDo",'a').write(query+"\n\n")
                self.write(dumps(handleNLPQuery(response)))
            else:
                open("unsatisfieldLogs",'a').write(
                    query+"\n\n"
                )
                self.write("nah")
        except tornado.web.MissingArgumentError :
            self.write(open("./frontend/main.html",'r').read())
        except Exception as e :
            open('errorLog','a').write(dumps(
                {
                    "query":query,
                    "error":str(e)
                },indent=4
            )+"\n\n")
            self.write(dumps(
                {
                    "mode":-2,
                    "body":[
                            "Sorry I couldnt understand your query"
                           ]

                }
            ))

class StaticFileHandler(tornado.web.StaticFileHandler):

    def write(self, chunk):
        super(StaticFileHandler, self).write(chunk)
        self.flush()


def initiate_server():
    return tornado.web.Application([
            (r"/",ChatbotServer),
            (r"/(.*)$",StaticFileHandler,{"path":"./frontend"})
        ])

if __name__=="__main__":
    if not(CONSOLE_MODE):
        server = initiate_server()
        server.listen(8080)
        tornado.ioloop.IOLoop.current().start()
        print("================================================================\n\nServer Initiated\n\n===========================================")
    else:
        print("Calling booobooo")
        while True :
            user_query = str(input("Your Question:"))
            pprint(handleNLPQuery(user_query))
