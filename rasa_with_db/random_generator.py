#!/usr/bin/python3

#from random import choice
from random import randint

def choice(sequence):
    return sequence[randint(0,len(sequence)-1)]

alphabets = 'abcdefghijklmnopqrstuvxyz'

def create_word():
    global alphabets
    out = ''
    for i in range(randint(3,8)):
        out+=choice(alphabets)
    return out

random_words=[create_word() for i in range(10000)]
print(random_words)

print(len(random_words))

def create_samples(skeleton,count):
    global random_words
    out=""
    for i in range(count):
        phrase = ""
        for j in range(randint(1,3)):
            phrase+=choice(random_words)+" "
        out+=skeleton%(phrase[:-1])+"\n"
    return out

nlu=""

nlu+="## intent:personQuery\n"

nlu+=create_samples("- who is [%s](target)",randint(50,60))

nlu+="\n\n## intent:personContact\n"

nlu+=create_samples("- where is [%s](target)",randint(50,60))

nlu+=create_samples("- what is the cabin number of [%s]",randint(50,60))

nlu+=create_samples("- what is the intercom number of [%s]",randint(50,60))

nlu+=create_samples("- how can i contact [%s](target)",randint(50,60))

nlu+=create_samples("- how to contact [%s](target)",randint(50,60))

nlu+=create_samples(" -contact [%s](target)",randint(50,60))

nlu+="\n\n## intent:objectQuery\n"

nlu+=create_samples("- what is [%s](target)",randint(50,60))
nlu+=create_samples("-what are the [%s](target)",randint(50,60))

open("nlu.md",'w').write(nlu)
