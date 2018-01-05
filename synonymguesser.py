#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synonymguesser.py
Created on Thu Dec 14 15:10:38 2017

@author: jamesp@speechmatics.com
"""



import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown


# a grammar for pulling out nouns
grNP = """
	NOUN:   {<PRP>?<JJ.*>*<NN.*>+}
    """


# find all the hyponyms of a noun, that is words that are
# more specific
def findHyponyms(n):
    h = []
    
    for synset in wn.synsets(n):
        h.append(synset.hyponyms())
    
    return h



def findFirstSynset(n):
    return wn.synsets(n)[0]




# performs NP-chunking to get the noun phrases (NPs) in a sentence, and
# return as a list of tuples
def getNouns(sentence):
    nouns = []
    tagged_sentence = nltk.pos_tag(sentence)
    parser = nltk.RegexpParser(grNP)
    tree = parser.parse(tagged_sentence)
 
    for subtree in tree.subtrees():
        if subtree.label() == 'NOUN': nouns.append(subtree.leaves()[0][0])
            
    return nouns





class SynonynGuesser:

   def __init__(self, text):
       self.numGuesses = 0
       self.text = text
      
   
    
   def guess(self):
       self.numGuesses += 1
       
       # split the text into tokens...
       tokens = nltk.word_tokenize(self.text)
       
       # now get the list of nouns...
       nouns = getNouns(tokens)
       for noun in nouns:
          print(noun)          
           
 
       # todo - score nouns by similartiy score
       # for each noun combination:
       #   n1.path_similarity(n2)
       # 
         
       
       return "cat"



