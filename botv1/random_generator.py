#!/usr/bin/python3

#from random import choice
from random import randint

def choice(sequence):
    return sequence[randint(0,len(sequence)-1)]

alphabets = 'abcdefghijklmnopqrstuvxyz'

def create_word():
    global alphabets
    out = ''
    for i in range(randint(3,14)):
        out+=choice(alphabets)
    return out

random_words=[create_word() for i in range(10000)]
print(random_words)

print(len(random_words))

def create_samples(skeleton,count,word_count_override=0):
    global random_words
    out=""
    for i in range(count):
        phrase = ""
        if word_count_override == 0 : #If word count not specified , it will take some random values between 1 to 3 for every phrase generation
            for j in range(randint(1,3)):
                phrase+=choice(random_words)+" "
            out+=skeleton%(phrase[:-1])+"\n"
        else:
            out+=skeleton%(choice(random_words))+"\n"
    return out

nlu=""

nlu+="## intent:personQuery\n"

nlu+=create_samples("- who is [%s](target)",randint(50,60))

nlu+="\n\n## intent:personContact\n"

nlu+=create_samples("- where is [%s](target)",randint(50,60))

nlu+=create_samples("- what is the cabin number of [%s](target)",randint(50,60))

nlu+=create_samples("- what is the intercom number of [%s](target)",randint(50,60))

nlu+=create_samples("- how can i contact [%s](target)",randint(50,60))

nlu+=create_samples("- how to contact [%s](target)",randint(50,60))

nlu+=create_samples(" -contact [%s](target)",randint(50,60))
nlu+=create_samples("- [%s](target) contact",randint(50,60))

nlu+="\n\n## intent:objectQuery\n"
nlu+=create_samples("- can i know [%s](target)",randint(50,60))
nlu+=create_samples("- can i know [%s](target)",randint(50,60))
nlu+=create_samples("- tell me about [%s](target)",randint(50,60))
nlu+=create_samples("- what is [%s](target)",randint(50,60))
nlu+=create_samples("-what are the [%s](target)",randint(50,60))

nlu+="\n\n## intent:courseQuery\n"
nlu+="""
- what are the courses available
- courses offered
- what are the courses offered
- courses available
- what are the programmes avaialble
- programmes available
- what are the programmes offered
- programmes offered
- programmes
- courses
"""
nlu+=create_samples("- what are the [%s](target) courses available",randint(50,60))
nlu+=create_samples("- [%s](target) courses offered",randint(50,60))
nlu+=create_samples("- [%s](target) courses available",randint(50,60))
nlu+=create_samples("- what are the [%s](target) programmes offered",randint(50,60))
nlu+=create_samples("- [%s](target) programmes offered",randint(50,60))
nlu+=create_samples("- [%s](target) programmes available",randint(50,60))

open("nlu.md",'w').write(nlu)
