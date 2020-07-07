#!/usr/bin/python3
from requests import get
from bs4 import BeautifulSoup , SoupStrainer

from pprint import pprint

import re

#htmlContent = get("https://vitap.ac.in/application-process-2/").text

#soup = BeautifulSoup(htmlContent,"lxml")

"""

The follwoing module extracts the sub parts in a page along with meta-info
like <div id=""> types

This is created as college suggested that the links in results should navigate to a specific part of page where the exact content is present

Hence ,College's website is modified in such a way that desired contents should be wrapped with a div tag with a unique id

"""


SOUP_FILTER = SoupStrainer('div',id=re.compile(".*"))

def searcher(soup :BeautifulSoup, url:str) -> tuple :
    """
    Returns list of subdiv tags whihc can be easily navigated , along with their meta data
    {
      "subPartsDetected":<bool> value
      "items" :[
        {
            "title":..
            "body":...
            "url":...
        },
        .
        .
        .

      ]
    }
    """
    num = 0
    while True :
        soup1 = soup.find("div",{"class":"col-md-12"})
        if(soup1==None):
            if(num==0):
                return {
                    "subPartsDetected" : False,
                    "items" : None
                }
                #return (False,None)
            else:
                break
        soup = soup1
        num+=1

    try:
        tags = (tag for tag in BeautifulSoup(str(soup),parse_only=SOUP_FILTER,features="lxml")) #Just throws up all the div tags with non null div ids

        out=[]
        for i in tags :
            title_tag = i.find(re.compile("h."))
            title="Nameless"

            if(title_tag==None):
                #print("My whole life was a lie")
                title_tag=i.find("strong")

            if(title_tag!=None):
                title=title_tag.text
            out.append({"title":title,"body":i.text,"url":url+"#"+i.get("id")})
        if(out!=None):
            #return (True,out)
            return{
                "subPartsDetected" : True,
                "items":out
            }
        else:
            return{
                    "subPartsDetected":False,
                    "items":None
            }
            #return (False,None)
    except Exception as e :
        return {
            "subPartsDetected":False,
            "items":None
        }
        #return (False,None)

if __name__=="__main__":
    pprint(searcher(BeautifulSoup(get("https://vitap.ac.in/fees-and-scholarship/").text,"lxml"),""))

