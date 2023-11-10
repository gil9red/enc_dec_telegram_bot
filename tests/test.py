#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import unittest
from commands import (
    text_to_bin,
    bin_to_text,
    text_to_hex,
    hex_to_text,
    text_to_base64,
    base64_to_text,
    text_to_ord,
    ord_to_text,
    from_ghbdtn,
    decode_escapes,
)


class CommandsTestCase(unittest.TestCase):
    def test_text_to_bin(self):
        expected = "Hello"
        self.assertEqual(
            "01001000 01100101 01101100 01101100 01101111", text_to_bin(expected)
        )
        self.assertEqual(expected, bin_to_text(text_to_bin(expected)))

        expected = "Привет"
        self.assertEqual(
            "11010000 10011111 11010001 10000000 "
            "11010000 10111000 11010000 10110010 "
            "11010000 10110101 11010001 10000010",
            text_to_bin(expected),
        )
        self.assertEqual(expected, bin_to_text(text_to_bin(expected)))

    def test_bin_to_text(self):
        self.assertEqual(
            "Hello", bin_to_text("01001000 01100101 01101100 01101100 01101111")
        )

        self.assertEqual(
            "Hello", bin_to_text("01001000 01100101\n01101100 01101100\n01101111")
        )

        self.assertEqual(
            "Привет",
            bin_to_text(
                "11010000 10011111 11010001 10000000 "
                "11010000 10111000 11010000 10110010 "
                "11010000 10110101 11010001 10000010",
            ),
        )

    def test_text_to_hex(self):
        expected = "Hello"
        self.assertEqual("48656c6c6f", text_to_hex(expected))
        self.assertEqual(expected, hex_to_text(text_to_hex(expected)))

        expected = "Привет"
        self.assertEqual(
            "d09fd180d0b8d0b2d0b5d182",
            text_to_hex(expected),
        )
        self.assertEqual(expected, hex_to_text(text_to_hex(expected)))

    def test_hex_to_text(self):
        self.assertEqual("Hello", hex_to_text("48656c6c6f"))

        self.assertEqual("Hello", hex_to_text("48 65 6c 6c\n6f"))

        self.assertEqual(
            "Привет",
            hex_to_text("d09fd180d0b8d0b2d0b5d182"),
        )

    def test_text_to_base64(self):
        expected = "Hello"
        self.assertEqual("SGVsbG8=", text_to_base64(expected))
        self.assertEqual(expected, base64_to_text(text_to_base64(expected)))

        expected = "Привет"
        self.assertEqual(
            "0J/RgNC40LLQtdGC",
            text_to_base64(expected),
        )
        self.assertEqual(expected, base64_to_text(text_to_base64(expected)))

    def test_base64_to_text(self):
        self.assertEqual("Hello", base64_to_text("SGVsbG8="))

        self.assertEqual(
            "Hello" * 4, base64_to_text("SGVsbG9 IZWxsb0h lbGxvSG\nVsbG8=")
        )

        self.assertEqual(
            "Привет",
            base64_to_text("0J/RgNC40LLQtdGC"),
        )

    def test_text_to_ord(self):
        expected = "Hello"
        self.assertEqual("[72, 101, 108, 108, 111]", text_to_ord(expected))
        self.assertEqual(expected, ord_to_text(text_to_ord(expected)))

        expected = "Привет"
        self.assertEqual(
            "[1055, 1088, 1080, 1074, 1077, 1090]",
            text_to_ord(expected),
        )
        self.assertEqual(expected, ord_to_text(text_to_ord(expected)))

    def test_ord_to_text(self):
        self.assertEqual("Hello", ord_to_text("[72, 101, 108, 108, 111]"))

        self.assertEqual("Hello", ord_to_text("[72, 101, 108,\n108, 111]"))

        self.assertEqual(
            "Привет",
            ord_to_text("[1055, 1088, 1080, 1074, 1077, 1090]"),
        )

    def test_from_ghbdtn(self):
        self.assertEqual("Привет", from_ghbdtn("Ghbdtn"))
        self.assertEqual(
            "И были проблемы с гостевой вроде бы, посмотри ",
            from_ghbdtn("B ,skb ghj,ktvs c ujcntdjq dhjlt ,s? gjcvjnhb "),
        )

    def test_decode_escapes(self):
        self.assertEqual(
            "2+2=4€ 😁",
            decode_escapes("\U00000032\U0000002b\x32=\U00000034&euro; \U0001F601"),
        )

        self.assertEqual("", decode_escapes(""))
        self.assertEqual("Hello", decode_escapes("Hello"))
        self.assertEqual("Привет!", decode_escapes("Привет!"))
        self.assertEqual("\n\r\t\b", decode_escapes(r"\n\r\t\b"))
        self.assertEqual("\U0001F601", decode_escapes(r"\U0001F601"))
        self.assertEqual("😁", decode_escapes(r"\U0001F601"))
        self.assertEqual("2+2=4", decode_escapes(r"\x32\x2B\x32=4"))
        self.assertEqual("2+2=4", decode_escapes(r"\x32\x2b\x32=\x34"))
        self.assertEqual("2+2=4", decode_escapes(r"\u0032\u002b\u0032=\u0034"))
        self.assertEqual(
            "2+2=4", decode_escapes(r"\U00000032\U0000002b\U00000032=\U00000034")
        )
        self.assertEqual("2+2=4", decode_escapes(r"\62\53\62\75\64"))
        self.assertEqual(
            "2+2=4", decode_escapes(r"\N{DIGIT TWO}+\N{DIGIT TWO}=\N{DIGIT FOUR}")
        )


if __name__ == "__main__":
    unittest.main()
