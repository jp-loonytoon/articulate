# -*- coding: utf-8 -*-
#
# SynonynGuesser.py - tries to guess a word
#   by an analysis of synonyms in the NPs of the sentence
#
# Author: jamesp@speechmatics.com
#
#
#


"""

Example usage::

    g = SynonynGuesser('This thing is a type of animal that has big ears.')
    word = g.guess()
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
            nouns.append(subtree.leaves()[0][0])

    return nouns


class SynonynGuesser:

    def __init__(self, text):
        self.numGuesses = 0
        self.text = text


    def getNouns(self):
        tokens = nltk.word_tokenize(self.text)

        return getNouns(tokens)


    def guess(self):
        bigrams = []
        terms = []
        prevNoun = ""
        n = 0

        self.numGuesses += 1

        nouns = getNouns(self)

        # get pairs of nouns (bigrams)
        for noun in nouns:
            if (n > 0):
                bigram = (wn.synsets(prevNoun)[0], wn.synsets(noun)[0])
                bigrams.append(bigram)
            prevNoun = noun
            n += 1

        # todo - score nouns by similartiy score
        for b in bigrams:
            lch = b[0].lowest_common_hypernyms(b[1])
            terms.append(lch)
            print(b)

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
