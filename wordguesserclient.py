#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wordguesserclient.py - client endpoint for word guesser WebSocket

Created on Wed Dec 13 14:15:37 2017

@author: jamesp@speechmatics.com

"""

from autobahn.twisted.websocket import WebSocketClientProtocol


class WordGuesserClientProtocol(WebSocketClientProtocol):

   def onOpen(self):
      self.sendMessage(u"Send data to guesser...".encode('utf8'))

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {0} bytes".format(len(payload)))
      else:
         print("Text message received: {0}".format(payload.decode('utf8')))