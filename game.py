# -*- coding: utf-8 -*-
#
# Game.py - controls the game by talking to the ASR and
# the word hypothesizer
#
# Author: jamesp@speechmatics.com
#
#
#


"""Starts a game of Articulate

Example usage::

    game = Game('wss://rt1.lab1.example.com:9000/')
    game.rounds = 3
    game.roundLength = 60
    game.start()
"""

import sys
import io
import yaml
import random

from twisted.python import log
from twisted.internet import reactor

from synonymguesser import SynonynGuesser
from inputtype import InputType

from sm_rtapi.rtapi import SpeechmaticsAPI
from sm_rtapi.exceptions import SpeechmaticsAPIError, SpeechmaticsAPIJobError
from sm_rtapi.recognitionconsumers.collecting import CollectingRecognitionConsumer
from sm_rtapi.audiosources.file import FileAudioSource
from sm_rtapi.audiosources.microphone import MicrophoneAudioSource



def startASR(apiUrl, lang, inputType=InputType.AUDIOFILE, inputFileName='example.wav'):
    """Start the Real-Time ASR.

    Args:
       apiUrl (string): The URI of the WebSocket to use for the Real-Time Appliance.
       lang (string): A language code as specified on the website. For example "en-US".
       inputType (InputType): InputType.MICROPHONE | InputType.AUDIOFILE
       inputFileName (string): Name of the audio file to use (used if InputType.AUDIOFILE)
    """

    transcriptChunk = ""

    try:
        api = SpeechmaticsAPI(apiUrl)
        consumer = CollectingRecognitionConsumer()

        if (inputType == InputType.AUDIOFILE):
            api.transcribe(FileAudioSource(inputFileName), lang, consumer)
        elif (inputType == InputType.MICROPHONE):
            api.transcribe(MicrophoneAudioSource(), lang, consumer)
        else:
            log.err("Bad input type " + inputType)
            sys.exit(3)

        api.run()

        if api.get_error() is not None:
            raise api.get_error()
        else:
            transcriptChunk = consumer.transcript

    except SpeechmaticsAPIJobError as e:
        log.err(e)
        sys.exit(2)
    except SpeechmaticsAPIError as e:
        log.err(e)
        sys.exit(1)

    return transcriptChunk


def readTextFile(ts):
    """Read input from a text file

    Args:
       ts (io.TextIOWrapper): The text file to use
    """

    try:
        transcriptChunk = ts.read().replace('\n', '')

    except IOError:
        print("Could not read file:")
        sys.exit()

    print(transcriptChunk)

    return transcriptChunk


guesserType = "synonym"  # random | synonym | corpus



class Game:

    def __init__(self, inputType):
        self.inputType = inputType
        self.input = None
        self.rounds = 1
        self.length = 60
        self.languageCode = 'en-US'
        self.words = []
        self.wsEndpoint = None

        log.startLogging(sys.stdout)



    def loadDictionary(self, dictionaryFile):
        with open(dictionaryFile, 'r') as f:
            try:
                for ln in f:
                    ln = ln.rstrip()
                    if (ln[0] != '['):
                        self.words.append(ln)

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
        log.msg("Input type = " + str(self.inputType))
        log.msg("Input = " + str(self.input))

        self.loadDictionary("dictionary.txt")
        transcript = ""

        if (self.inputType == InputType.MICROPHONE):
            # 1a. process text from speech using Real-Time ASR session...
            transcript = startASR(self.wsEndpoint, self.languageCode, self.inputType)
        elif (self.inputType == InputType.AUDIOFILE):
            # 1b. process text from audio file using Real-Time ASR session...
            log.msg("Audio file = " + str(self.input.name))
            transcript = startASR(self.wsEndpoint, self.languageCode, self.inputType, str(self.input.name))
        elif (self.inputType == InputType.TEXTFILE):
            # 1c. read in the text from a file...
            transcript = readTextFile(self.input)

        log.msg("Transcript: " + transcript)

        # 2. choose a guesser and start feeding it transcribed phrases
        self.guessTranscript(transcript)



    def stop(self):
        reactor.stop()




if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))

    # create a new game and pass it a text file with the transcript
    game = Game(InputType.TEXTFILE)
    game.input = io.open('example.txt', mode="r", encoding="utf-8")
    game.rounds = config['numrounds']
    game.roundLength = config['roundlength']
    game.wordlist = config['dictionary']
    game.start()
