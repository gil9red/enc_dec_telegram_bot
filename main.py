#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import enum
import os
import time

from typing import Callable

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
    Defaults,
    CallbackQueryHandler,
)

from config import TOKEN, DIR_LOGS
from commands import (
    text_to_base64,
    base64_to_text,
    text_to_hex,
    hex_to_text,
    text_to_bin,
    bin_to_text,
    text_to_ord,
    ord_to_text,
    from_ghbdtn,
    decode_escapes,
)
from common import get_logger, log_func, reply_error


class CommandEnum(enum.Enum):
    text_to_base64 = ("text -> base64", text_to_base64)
    base64_to_text = ("base64 -> text", base64_to_text)
    text_to_hex = ("text -> hex", text_to_hex)
    hex_to_text = ("hex -> text", hex_to_text)
    text_to_bin = ("text -> bin", text_to_bin)
    bin_to_text = ("bin -> text", bin_to_text)
    text_to_ord = ("text -> ord", text_to_ord)
    ord_to_text = ("ord -> text", ord_to_text)
    from_ghbdtn = ("ghbdtn -> привет", from_ghbdtn)
    decode_escapes = ("decode escapes", decode_escapes)

    def __init__(self, title: str, func: Callable[[str], str]):
        self.title = title
        self.func = func

    def __call__(self, *args, **kwargs) -> str:
        return self.func(*args, **kwargs)

    def get_button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(self.title, callback_data=self.name)


REPLY_MARKUP = InlineKeyboardMarkup([
    [
        CommandEnum.text_to_base64.get_button(),
        CommandEnum.base64_to_text.get_button(),
    ],
    [
        CommandEnum.text_to_hex.get_button(),
        CommandEnum.hex_to_text.get_button(),
    ],
    [
        CommandEnum.text_to_bin.get_button(),
        CommandEnum.bin_to_text.get_button(),
    ],
    [
        CommandEnum.text_to_ord.get_button(),
        CommandEnum.ord_to_text.get_button(),
    ],
    [
        CommandEnum.from_ghbdtn.get_button(),
    ],
    [
        CommandEnum.decode_escapes.get_button(),
    ],
    [
        InlineKeyboardButton("reset", callback_data='reset'),
    ]
])


log = get_logger(__file__, DIR_LOGS / "log.txt")


@log_func(log)
def on_start(update: Update, _: CallbackContext):
    update.effective_message.reply_text(
        "Bot for encoding/decoding to/from Base64/hex/bin. Support only UTF-8 encoding.\n"
        "Enter something and click on the button"
    )


@log_func(log)
def on_request(update: Update, _: CallbackContext):
    message = update.effective_message

    message.reply_text(
        message.text,
        reply_markup=REPLY_MARKUP,
        quote=True,
        disable_web_page_preview=True,
    )


@log_func(log)
def on_callback_query(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()

    query_text = query.data
    prev_text = text = query.message.text
    try:
        if query_text == "reset":
            text = query.message.reply_to_message.text
        else:
            command = CommandEnum[query_text]
            text = command(text)

        if len(text) > 4096:
            raise Exception("The resulting text is more than 4096 characters!")

    except KeyError:
        raise Exception(f"Unsupported command {query_text!r}!")

    except Exception as e:
        log.exception("Error:")
        text = f"⚠ Error: {e}"

    if prev_text != text:
        query.message.edit_text(
            text,
            reply_markup=REPLY_MARKUP,
            disable_web_page_preview=True,
        )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    log.debug("Start")

    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug(f"System: CPU_COUNT={cpu_count}, WORKERS={workers}")

    updater = Updater(
        TOKEN,
        workers=workers,
        defaults=Defaults(run_async=True),
    )
    bot = updater.bot
    log.debug(f"Bot name {bot.first_name!r} ({bot.name})")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", on_start))
    dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(CallbackQueryHandler(on_callback_query))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug("Finish")


if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            log.exception("")

            timeout = 15
            log.info(f"Restarting the bot after {timeout} seconds")
            time.sleep(timeout)
