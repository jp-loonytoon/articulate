#!/usr/bin/env python

# inputtype.py - enum for the possible input types for the
# articulate game:
#
#   MICROPHONE | AUDIOFILE | TEXTFILE | STDIO
#
# Usage:
#   if (args.microphone):
#       inputType = InputType.MICROPHONE
#
# Author: jamesp@speechmatics.com
#
#
#


from enum import Enum


class InputType(Enum):
    MICROPHONE = 1
    AUDIOFILE = 2
    TEXTFILE = 3
    STDIO = 4
