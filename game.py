#!/usr/bin/env python

# Game.py - controls the game by talking to the ASR and
# the word hypothesizer
#
# Author: jamesp@speechmatics.com
#
#
#

import sys
import yaml
import random

from SpeechmaticsAPI import SpeechmaticsAPI, SpeechmaticsAPIError, SpeechmaticsAPIJobError
from SpeechmaticsAPI.RecognitionConsumers.PrintingRecognitionConsumer import PrintingRecognitionConsumer
from SpeechmaticsAPI.RecognitionConsumers.CollectingRecognitionConsumer import CollectingRecognitionConsumer
from SpeechmaticsAPI.AudioSources.MicrophoneAudioSource import MicrophoneAudioSource
from SpeechmaticsAPI.AudioSources.FileAudioSource import FileAudioSource

from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory
from wordguesserclient import WordGuesserClientProtocol

from synonymguesser import SynonynGuesser




def startASR(apiUrl, lang):
    
    log.msg("API URL: ", apiUrl)
    log.msg("Language: ", lang)
    
    filename = "example.wav"
    
    try:
        api = SpeechmaticsAPI(apiUrl)
        # api.transcribe(FileAudioSource(filename), lang, CollectingRecognitionConsumer())
        # api.transcribe(FileAudioSource(filename), lang, PrintingRecognitionConsumer())
        # api.transcribe(MicrophoneAudioSource(), lang, PrintingRecognitionConsumer())
        api.run()
        
        if api.getError() != None:
            raise api.getError()

    except SpeechmaticsAPIJobError as e:
        log.err(e)
        sys.exit(2)
    except SpeechmaticsAPIError as e:
        log.err(e)
        sys.exit(1)



def startGuesserClient():
    factory = WebSocketClientFactory()
    factory.protocol = WordGuesserClientProtocol
    reactor.connectTCP("localhost", 9002, factory)
    reactor.run()



guesserType = "synonym"      # random | synonym | corpus



class Game:

   def __init__(self, rtaUrl):
      self.rounds = 1
      self.length = 60
      self.languageCode = 'en-US'
      self.words = []
      self.wsEndpoint = rtaUrl
      log.startLogging(sys.stdout)


   def loadDictionary(self, dictionaryFile):
      with open(dictionaryFile,'r') as f:
          try:
              for ln in f:
                  ln = ln.rstrip()
                  if (ln[0] != '['):
                     self.words.append(ln)

              for w in self.words:
                  print(w)
              
          except IOError:
             print("Could not read file:", dictionaryFile)
             sys.exit()
             

   # a random word guesser (for comparative testing)
   def guessTranscriptRandom(self, transcript):
       targetWord = ""
       
       if len(self.words) > 0:
           targetWord = random.choice(self.words)
           
       return targetWord
   

   # a synonym word guesser
   def guessTranscriptSynonym(self, transcript):
       synGuesser = SynonynGuesser(transcript)
       targetWord = synGuesser.guess()

       return targetWord
   
    
   # a corpus-based word guesser
   def guessTranscriptCorpus(self, transcript):
       targetWord = ""
       
       # TODO: use a corpus search to find target word
           
       return targetWord


   
   def guessTranscript(self, transcript):
       if guesserType == "random":
           targetWord = self.guessTranscriptRandom(transcript)
       elif guesserType == "synonym":
           targetWord = self.guessTranscriptSynonym(transcript)          
       elif guesserType == "corpus":
           targetWord = self.guessTranscriptCorpus(transcript) 
       else:
          log.err("Unrecognised guesser: ", guesserType)
          
          
       print("The word guessed is: %s" % targetWord)
    
    
    
    

   def start(self):
       log.msg("Starting a game of %d rounds" % (self.rounds))
       self.loadDictionary("dictionary.txt")

       # 1. open an Real-Time ASR session and start transcribing
       startASR(self.wsEndpoint, self.languageCode)

       # 2. choose a guesser and start feeding it transcribed phrases
       log.msg("Openning connection to Guesser: %s" % (guesserType))
       #startGuesserClient()
      
       s1 = "This is a type of animal that has whiskers and purrs. They like milk."
       s2 = "This city is the capital of France."
       
       self.guessTranscript(s1)
       self.guessTranscript(s2)


   def stop(self):
       reactor.stop()





if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))

    # create a new game
    game = Game(config['rtaUrl'])
    game.rounds = config['numrounds']
    game.roundLength = config['roundlength']
    game.wordlist = config['dictionary']
    game.start()