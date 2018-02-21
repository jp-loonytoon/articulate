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
        if subtree.label() == 'NOUN':
            for l in subtree.leaves():
                if (l[1] == 'NN' or l[1] == 'NNS'):
                    print(l[0])
                    nouns.append(l[0]) 

    return nouns


class SynonynGuesser:

    def __init__(self, text):
        self.numGuesses = 0
        self.text = text

    def guess(self):
        self.numGuesses += 1
        bigrams = []
        terms = []
        prevNoun = ""
        n = 0

        # split the text into tokens...
        tokens = nltk.word_tokenize(self.text)

        # now get the list of nouns...
        nouns = getNouns(tokens)

        # get pairs of nouns (bigrams)
        for noun in nouns:
            print("Noun = " + noun)
            if (n > 0):
                bigram = (wn.synsets(prevNoun)[0], wn.synsets(noun)[0])
                bigrams.append(bigram)
            prevNoun = noun
            n += 1

        # todo - score nouns by similartiy score
        for b in bigrams:
            lch = b[0].lowest_common_hypernyms(b[1])
            terms.append(lch)

        # find the lowest single hypernym that is shared by the bigram
        # store them in a list and return the most frequent
        # if there is no one that is most frequent, return the first one
        # as best guess

        # for each noun combination:
        #   n1.path_similarity(n2)
        #
        for t in terms:
            print(t)

        return "rabbit"



if __name__ == '__main__':
    transcript = "This animal is a type of rodent; it has big teeth and long floppy ears."
    
    synGuesser = SynonynGuesser(transcript)
    targetWord = synGuesser.guess()
    
    print(targetWord)