#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import json

from third_party.bin2str import str2bin as text_to_bin, bin2str as bin_to_text
from third_party.swap_keyboard import swap_keyboard
from third_party.decode_escapes_telegram_bot.utils import decode as decode_escapes


ENCODING = "utf-8"
ERRORS = "replace"


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
    return "".join(chr(x) for x in items)


if __name__ == "__main__":
    assert base64_to_text(text_to_base64("Hello")) == "Hello"
    assert hex_to_text(text_to_hex("Hello")) == "Hello"
    assert bin_to_text(text_to_bin("Hello")) == "Hello"
    assert ord_to_text(text_to_ord("Привет")) == "Привет"
    assert swap_keyboard("Ghbdtn") == "Привет"
    assert swap_keyboard("Руддщ") == "Hello"
    assert (
        decode_escapes("\U00000032\U0000002b\x32=\U00000034&euro; \U0001F601")
        == "2+2=4€ 😁"
    )
