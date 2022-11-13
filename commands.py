#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
import json


ENCODING = 'utf-8'
ERRORS = 'replace'


def text_to_base64(text: str) -> str:
    data = text.encode(encoding=ENCODING, errors=ERRORS)
    return base64.b64encode(data).decode(encoding=ENCODING, errors=ERRORS)


def base64_to_text(text: str) -> str:
    return base64.b64decode(text).decode(encoding=ENCODING, errors=ERRORS)


def text_to_hex(text: str) -> str:
    return text.encode(encoding=ENCODING, errors=ERRORS).hex()


def hex_to_text(text: str) -> str:
    return bytes.fromhex(text).decode(encoding=ENCODING, errors=ERRORS)


def text_to_ord(text: str) -> str:
    items = [ord(c) for c in text]
    return json.dumps(items)


def ord_to_text(text: str) -> str:
    items = json.loads(text)
    return ''.join(chr(x) for x in items)
