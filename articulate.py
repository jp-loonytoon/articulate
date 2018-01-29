#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
articulate.py - the main entry point for the game,
responsible for starting all the necessary services

Created on Wed Dec 13 14:15:37 2017

@author: jamesp@speechmatics.com

"""

import yaml
import argparse
import sys
from game import Game
from inputtype import InputType



""" the game should support the following ways of getting text in to the
Game object:
    
    typing (stdio)
    speech (via RTA Speech API)
    audio file (via RTA Speech API)
    
    Usage: articulate [options]
    
    An Articulate game player for that demonstrates real-time ASR 
    and NLP techniques.
    
    Options include:
        -m             use microphone audio input (requires use of an RTA)
        -w [uri]       use Websocket URI to connet to RTA
        -a [filename]  use file audio input (requires use of an RTA)
        -t [filename]  use text file input
        -s             use stdio for keyboard input
        -c [filename]  take configuration from YAML file
    
"""

if __name__ == '__main__':
    # create a arg parser to process cmdline
    parser = argparse.ArgumentParser(description='An Articulate game player for that demonstrates real-time ASR and NLP techniques.')
    parser.add_argument('-m', '--microphone', action='store_true', help='use microphone audio input (requires use of an RTA)')
    parser.add_argument('-w', '--websocket', help='use Websocket URI to connet to RTA')
    parser.add_argument('-a', '--audiofile', type=argparse.FileType('rb'), help='use file audio input (requires use of an RTA)')
    parser.add_argument('-t', '--textfile', type=argparse.FileType('r'), help='use text file input')
    parser.add_argument('-s', '--stdin', help='use stdio for keyboard input')
    parser.add_argument('-c', '--configfile', default='config.yml', type=argparse.FileType('r'), help='use text file input')

    args = parser.parse_args()
    config = yaml.safe_load(args.configfile)

    # the websockets URI for connection to an RTA can be
    # read from the command-line or a config file. If no
    # websockets URI is specified, then text file or stdin
    # are the only mechanisms that can be used to input
    # text to the game
    if (args.websocket):
        rtaUrl = args.websocket
    else:
        rtaUrl = config['rtaUrl']

    # defines which input type of text will be used
    if (args.microphone):
        inputType = InputType.MICROPHONE
    elif (args.audiofile):
        inputType = InputType.AUDIOFILE
    elif (args.textfile):
        inputType = InputType.TEXTFILE
    else:
        inputType = InputType.STDIO

    # create a new game
    game = Game(inputType)

    game.wsEndpoint = rtaUrl
    game.rounds = config['numrounds']
    game.roundLength = config['roundlength']
    game.wordlist = config['dictionary']

    try:
        if inputType == InputType.AUDIOFILE:
            game.input = args.audiofile
        if inputType == InputType.TEXTFILE:
            game.input = args.textfile
        if inputType == InputType.STDIO:
            game.input = sys.stdio
    except NameError:
        print("Input not defined for " + inputType)
    else:
        game.start()
