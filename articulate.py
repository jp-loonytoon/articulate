#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
articulate.py - the main entry point for the game,
responsible for starting all the necessary services

Created on Wed Dec 13 14:15:37 2017

@author: jamesp@speechmatics.com

"""

import yaml
from game import Game



if __name__ == '__main__':
    config = yaml.safe_load(open("config.yml"))

    # create a new game
    game = Game(config['rtaUrl'])
    game.rounds = config['numrounds']
    game.roundLength = config['roundlength']
    game.wordlist = config['dictionary']
    game.start()
    