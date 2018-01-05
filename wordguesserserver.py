#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wordguesserserver.py - server endpoint for word guesser WebSocket

Created on Wed Dec 13 14:15:37 2017

@author: jamesp@speechmatics.com

"""


import yaml
import sys
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor



def loadDictionary(wordlistFile):
    wl = []
    
    try:
        f = open(wordlistFile, "r")
        log.msg("Loaded dictionary file")
        wl = f.readlines()
    except IOError as e:
        log.err("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        e = sys.exc_info()[0]
        log.err("Unexpected error:", e)
        sys.exit(e)
        
    return wl
            



class WordGuesserServerProtocol(WebSocketServerProtocol):
    

    def __init__(self):
        log.startLogging(sys.stdout)
        config = yaml.safe_load(open("config.yml"))
        self.words = loadDictionary(config['dictionary'])
        WebSocketServerProtocol.__init__(self)


            
    def pickWord(self):
        return self.words[1]


    def printDictionary(self):
        for w in self.words:
            print(w)            
    
            

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        print("WebSocket connection open.")


    def onMessage(self, payload, isBinary):
        try:
            word = self.pickWord()
        
            if isBinary:
                log.msg("Binary message received: {0} bytes".format(len(payload)))
            else:
                log.msg("Text message received: {0}".format(payload.decode('utf8')))

            # echo back message verbatim
            self.sendMessage(word, not isBinary)
            
        except:
            e = sys.exc_info()[0]
            log.err(e)


    def onClose(self, wasClean, code, reason):
        log.msg("WebSocket connection closed: {0}".format(reason))



if __name__ == '__main__':
   log.startLogging(sys.stdout)
   factory = WebSocketServerFactory()
   factory.protocol = WordGuesserServerProtocol

   reactor.listenTCP(9002, factory)
   reactor.run()
