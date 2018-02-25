#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synonymguesser.py
Created on Thu Dec 14 15:10:38 2017
@author: jamesp@speechmatics.com
"""

import nltk
from nltk.corpus import wordnet as wn

# a grammar for pulling out nouns
GR_NP = """
    NOUN:   {<PRP>?<JJ.*>*<NN.*>+}
    """


def get_nouns(sentence):
    """Performs NP-chunking to get the nouns in a sentence, 
    and return as a list of words
    
    Args:
        sentence (str): The sentence to parse.
        
    Returns:
        list: nouns in the sentence."""
    
    nouns = []
    
    tagged_sentence = nltk.pos_tag(sentence)
    parser = nltk.RegexpParser(GR_NP)
    tree = parser.parse(tagged_sentence)

    for subtree in tree.subtrees():
        if subtree.label() == 'NOUN':
            for l in subtree.leaves():
                if l[1] == 'NN' or l[1] == 'NNS':
                    nouns.append(l[0])

    return nouns




class SynonynGuesser:
    """A guesser that bases its hypotheses on finding synonyms.
    
    Args:
        text (str): The initial paragraph to base the guess on.
        
    Attributes:
        numGuesses (int): The number of guesses that have been made.
        text (str): The whole text no which to base the guesses.
    """
        

    def __init__(self, text):
        self.numGuesses = 0
        self.text = text

    def guess(self):
        self.numGuesses += 1

        # split the text into tokens...
        tokens = nltk.word_tokenize(self.text)

        # now get the list of nouns...
        nouns = get_nouns(tokens)

        # now build a list of hypernyms for these nouns
        hypernyms = []
        for n in nouns:
            for syn in wn.synsets(n):
                hypernyms.append(syn.hypernyms())

        # and pick the most common hyponym
        hyponyms = []
        for h in hypernyms:
            for s in h:
                for ho in s.hyponyms():
                    # weed out any words that are in the text itself
                    if (ho.lemma_names()[0]) not in set(tokens):
                        hyponyms.append(ho)

        # find the most frequent hyponym
        commonestHyponym = max(set(hyponyms), key=hyponyms.count)
        
        likelyWord = commonestHyponym.lemma_names()[0]

        return likelyWord



if __name__ == '__main__':
    TRANSCRIPT = "A big ship that sank in 1912 because it hit an iceberg."

    synGuesser = SynonynGuesser(TRANSCRIPT)
    targetWord = synGuesser.guess()

    print(targetWord)
    
