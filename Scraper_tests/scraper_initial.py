#!/usr/bin/python3

from termcolor import cprint
from requests import get
from bs4 import BeautifulSoup
import threading
from queue import Queue
import time
import functools
from pprint import pprint
from datetime import datetime
from os import system
from os.path import isdir
from json import loads
from json import dumps
import pickle
from string import printable

NumberOfThreads=10 #Change the number here to increase the thread count

thread_flags=[False]*NumberOfThreads

improper_sites=[]
titles=[]
#Initializing The Queue which handles the Links
Links_Queue=Queue()
#Links_Queue.put("https://vitap.ac.in/campus-life/clubs-chapters/nggallery/clubs-and-chapters/UDDESHYA/slideshow")
Links_Queue.put("https://vitap.ac.in/international-credit-transfer-between-vit-ap-and-asu/")
#Collected_Links=["https://vitap.ac.in/international-credit-transfer-between-vit-ap-and-asu/","https://vitap.ac.in/campus-life/clubs-chapters/nggallery/clubs-and-chapters/UDDESHYA/slideshow"]
Collected_Links=["https://vitap.ac.in/international-credit-transfer-between-vit-ap-and-asu/"]

Collected_Links_httpless=["vitap.ac.in/international-credit-transfer-between-vit-ap-and-asu/"]

Spell_Check_Corpus=dict()

Html_with_newline = ["p","h1","h2","h3","h4","h5","li","br"] #Tags content to be cured and speerated by newline
Html_with_Space=["th",'td','tr']

punctuations = ["\"","\n","+","=","!","@","#","$","%","^","&","*","(",")","{","}",",",". ","\t",":",";","<",">","/","\\","~"] # used in string to word converter

path=""

def Print(inp_str):
    if __name__=="__main__":
        print(inp_str)

class InabilityToModifyError(Exception):
    pass

def cureContent(inp_str): #Cleans unicode Charecters from ascii by replacing it with space charecter
    out=""
    for i in inp_str :
        if i not in printable[:-3] :
            out+=" "
        else:
            out+=i
    return out.lower()

def setScraperDestPath(inp_str):
    global path
    path=inp_str
    if(isdir(path+"_new/")):
        print("Directory Exists.. Attempting to Delete")
        if(system("rm -r "+path+"_new/")!=0):
            raise InabilityToModifyError("Probably Requires Root Permisions")
        else:
            if(system("mkdir "+path+"_new")!=0):
                raise InabilityToModifyError("Probablye Requires Root Permisions")
    else:
        if(system("mkdir "+path+"_new")!=0):
            raise InabilityToModifyError("Probablye Requires Root Permisions")
    print("Path Customized")

def get_all_links(soup_text):
    gathered_links=[]
    start_link=soup_text.find("a href")
    while start_link!=-1 :
        start_quote = soup_text.find('"', start_link)
        end_quote = soup_text.find('"', start_quote + 1)
        url = soup_text[start_quote + 1: end_quote]
        gathered_links.append(url)
        soup_text=soup_text[end_quote:]
        start_link=soup_text.find("a href")
    return gathered_links

#Function Which extracts WebContent for a given link.. (It is designed for VITAP Website dated October 2019)
def extract_content(link):
    global improper_sites, Html_with_Space ,Html_with_newline

    http_request = get(link)
    if (link!=http_request.url) : #The filter is being applied to avoid rediretive links , as redirective links are resuting in duplicated data
        return (None,None,[])

    soup=BeautifulSoup(http_request.text,'lxml')

    links2=soup.findAll('a')
    links2=[x.get("href") for x in links2]

    maniac=""
    try:
        title=soup.title.string
        main_content=soup.find("body").find("div",attrs={"id":"page"})
        main_content=main_content.find("div",attrs={"class":"site-content-contain"})
        main_content=main_content.find("div",attrs={"class":"site-content"})
        main_content=main_content.find("section",attrs="pages")
        main_content=main_content.find("div",attrs={"container"})
        main_content=main_content.find("div",attrs={"row"})
        sub_contents=main_content.findAll("div")
        for i in sub_contents :
            try:

                if "col-md-4" not in i.get("class") :
                    try:
                        i.script.decompose()
                        print("Check it out")
                    except AttributeError :
                        pass

                    #Cleaning the HTML Tags
                    for j in Html_with_newline:
                        try:
                            for k in i.findAll(j):
                                k.replaceWith(k.text+"\n")
                        except Exception :
                            pass

                    for j in Html_with_Space :
                        try :
                            for k in i.findAll(j):
                                k.replaceWith(k.text+"  ")
                        except Exception :
                            pass

                    maniac+=i.getText()+"\n\n"

            except Exception as e :
                pass
                #links2=get_all_links(str(soup))
        return(cureContent(title),cureContent(maniac),links2)
    except AttributeError :
        Print("Website Aint Parseable")
        improper_sites.append(link)
        return(None,None,links2)

def synchronized(wrapped):
    lock = threading.Lock()
    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        #print "Calling '%s' with Lock %s" % (wrapped.__name__, id(lock))
        with lock:
            return wrapped(*args, **kwargs)
    return _wrap


#Thread functions and Classes
@synchronized
def CanIWait():
    global thread_flags
    status=False
    for i in thread_flags:
        status|=i
    return status

linksCount=0

@synchronized
def titleOperation(inp,mode):
    global titles
    if mode == 0 :
        return inp in titles
    else:
        titles.append(inp)

@synchronized
def strToWords(inp_str,word_length_override=False):  #Converts string to words for error correction features
    global punctuations , Spell_Check_Corpus

    for i in punctuations :
        inp_str = inp_str.replace(i,' ')
    inter_words=inp_str.lower().replace('  ',' ').split(' ')

    for i in inter_words :
        if(not(i.isnumeric()) and (word_length_override or len(i)>=4)) :
            if(i in Spell_Check_Corpus):
                Spell_Check_Corpus[i]+=1
            else:
                Spell_Check_Corpus[i]=1



@synchronized
def writeTofile(title,link,content):
    global linksCount
    with open(path+"_new/%d"%(linksCount),"w") as File :
        File.write(dumps(({'title':title,"link":link,"content":content}),indent=4))
    strToWords(title,word_length_override=True)
    strToWords(content)
    linksCount+=1


@synchronized
def AddLink(inp_link):
    global Collected_Links
    global Collected_Links_httpless
    global Links_Queue
    if (("https://vitap.ac.in" == inp_link[:19]) or ("http://vitap.ac.in" == inp_link[:18])) and (inp_link.split("//")[-1] not in Collected_Links_httpless) and ("mailto" not in inp_link) and ("/wp-content/" not in inp_link) and ("/gallery" not in inp_link) :
        Links_Queue.put(inp_link)
        Collected_Links.append(inp_link)
        Collected_Links_httpless.append(inp_link.split("//")[-1])

class ScraperThread(threading.Thread):

    def __init__(self,thrdNo):
        self.thrdNo=thrdNo
        threading.Thread.__init__(self)
        self.t=0
        if thrdNo == 0 :
            self.t=time.time()
    def getLinkFromQueue(self):
        global Links_Queue
        global thread_flags
        try:
            link=Links_Queue.get(True,2)
            thread_flags[self.thrdNo]=True
            return link
        except Exception as e:
            thread_flags[self.thrdNo]=False
            if CanIWait() :
                return self.getLinkFromQueue()
            else:
                return None #Thread should get ready to kill itself

    def run(self):
        global linksCount
        global improper_sites
        while True :
            link=self.getLinkFromQueue()
            if link!=None :     #Thread Kill Condition when Link in None
                title,content,links=extract_content(link)

                if(title!=None and not(titleOperation(title,0))):
                    writeTofile(title,link,content)
                    titleOperation(title,1)
                else:
                    Print("Link Parsed:"+str(link))

                for i in links:
                    AddLink(i)

                Print("Links Handled:"+str(linksCount))
            else:
                break
        print("Thread Number %d Closed"%(self.thrdNo))
        Print(str(len(Collected_Links))+" "+str(len(set(Collected_Links))))
        if self.thrdNo==0 :
            self.t=time.time()-self.t
            cprint("Took %d to scrape"%(self.t),'yellow')
            Print(str(improper_sites))
            with open(path+"_new/word_corpus",'w') as File :
                File.write(dumps((Spell_Check_Corpus),indent=4))
            with open(path+"_new/word_corpus.bin",'wb') as File :
                pickle.dump(Spell_Check_Corpus, File)
            system("rm -r "+path)
            system("mv %s_new %s"%(path,path))
            time.sleep(5)
            pprint(Collected_Links)

threads=[]

def initiateScraper():
    global threads
    for i in range(NumberOfThreads):
        threads.append(ScraperThread(i))
        threads[-1].start()

if __name__=="__main__":
    setScraperDestPath("/home/ubuntu/Scraped_files")
    initiateScraper()
