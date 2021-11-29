#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import base64
import os
import time

# pip install python-telegram-bot
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater, MessageHandler, CommandHandler, Filters, CallbackContext, Defaults, CallbackQueryHandler
)

from config import TOKEN, DIR_LOGS
from common import get_logger, log_func, reply_error


REPLY_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("text -> base64", callback_data='text_to_base64'),
        InlineKeyboardButton("base64 -> text", callback_data='base64_to_text'),
    ],
    [
        InlineKeyboardButton("text -> hex", callback_data='text_to_hex'),
        InlineKeyboardButton("hex -> text", callback_data='hex_to_text'),
    ],
    [
        InlineKeyboardButton("reset", callback_data='reset'),
    ]
])

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


log = get_logger(__file__, DIR_LOGS / 'log.txt')


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Bot for encoding/decoding to/from Base64/HEX. Support only UTF-8 encoding.\n'
        'Enter something and click on the button'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        message.text,
        reply_markup=REPLY_MARKUP,
        quote=True
    )


@log_func(log)
def on_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    prev_text = text = query.message.text
    try:
        match query.data:
            case 'text_to_base64':
                text = text_to_base64(text)
            case 'base64_to_text':
                text = base64_to_text(text)
            case 'text_to_hex':
                text = text_to_hex(text)
            case 'hex_to_text':
                text = hex_to_text(text)
            case 'reset':
                text = query.message.reply_to_message.text
            case _:
                raise Exception(f'Unsupported command {query.data!r}!')

        if len(text) > 4096:
            raise Exception('The resulting text is more than 4096 characters!')

    except Exception as e:
        text = f'⚠ Error: {e}'

    if prev_text != text:
        query.message.edit_text(text, reply_markup=REPLY_MARKUP)


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    log.debug('Start')

    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug(f'System: CPU_COUNT={cpu_count}, WORKERS={workers}')

    updater = Updater(
        TOKEN,
        workers=workers,
        defaults=Defaults(run_async=True),
    )
    bot = updater.bot
    log.debug(f'Bot name {bot.first_name!r} ({bot.name})')

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(MessageHandler(Filters.text, on_request))
    dp.add_handler(CallbackQueryHandler(on_callback_query))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
