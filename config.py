#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

from pathlib import Path


# Current folder where the script is located
DIR = Path(__file__).resolve().parent

DIR_LOGS = DIR / 'logs'
DIR_LOGS.mkdir(parents=True, exist_ok=True)

TOKEN_FILE_NAME = DIR / 'TOKEN.txt'

try:
    TOKEN = os.environ.get('TOKEN') or TOKEN_FILE_NAME.read_text('utf-8').strip()
    if not TOKEN:
        raise Exception('TOKEN is empty!')

except:
    print(f'You need to add the bot token to {TOKEN_FILE_NAME.name} or to the TOKEN environment variable')
    TOKEN_FILE_NAME.touch()
    sys.exit()

ERROR_TEXT = '⚠ There was some problem. Please try again or try a little later...'
