#!/usr/bin/env python
# encoding: utf-8

from sre_constants import BRANCH, SUBPATTERN
from sre_compile import compile as sre_compile
from sre_parse import Pattern, SubPattern, parse
import sys


PYTHON_VERSION = sys.version_info.major
PYTHON_VERSION_LESS_THAN_3 = PYTHON_VERSION < 3


# scanner
class Scanner:
    def __init__(self, lexicon, flags=0):
        self.lexicon = []
        p = []
        s = Pattern()
        s.flags = flags
        if PYTHON_VERSION_LESS_THAN_3:
            s.groups = len(lexicon) + 1
            for group, (phrase, name) in enumerate(lexicon, 1):
                p.append(SubPattern(s, [(SUBPATTERN, (group, parse(phrase, flags))), ]))
                self.lexicon.append((group-1, name))
        else:
            self.lexicon = lexicon
            for phrase, name in lexicon:
                gid = s.opengroup()
                p.append(SubPattern(s, [(SUBPATTERN, (gid, 0, 0, parse(phrase, flags))), ]))
                s.closegroup(gid, p[-1])

        p = SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile(p).scanner

    def scan(self, string):
        match = self.scanner(string).match
        start_idx = 0
        token_num = 0
        start_flag = False
        breakaway_counter = 0
        while start_idx < len(string):
            matches = [m for m in iter(match, None)]
            for m in matches:
                if start_flag:
                    unknown_start_idx = m.start()
                    unknown_start_encoding = string[start_idx:unknown_start_idx]
                    if len(unknown_start_encoding):
                        yield 'UNKNOWN', unknown_start_encoding, token_num, (start_idx, unknown_start_idx)
                        token_num += 1
                    start_flag = False
                    start_idx = unknown_start_idx
                    breakaway_counter = 0

                grp_name = self.lexicon[m.lastindex - 1][1]
                end_idx = m.end()
                if grp_name:
                    word = string[start_idx:end_idx]
                    yield grp_name, word, token_num, (start_idx, end_idx)
                    token_num += 1
                start_idx = end_idx
            breakaway_counter += 1
            # break after 10 continuous characters which doesn't many any pattern
            if breakaway_counter > 10:
                break
            start_flag = True


# patterns
heb = r"[א-ת]" + "{1,}[\']?[\"]*" + "[א-ת]" + "{1,}|" + "[א-ת]"
eng = r"[a-zA-Z]{1,}[\']?[\"]*[a-zA-Z0-9]{1,}|[a-zA-Z][a-zA-Z0-9]*"
hour = r"[0-2]?[0-9]:[0-5][0-9]"
date1 = r"[0-9]{1,3}-[0-9]{1,3}-([1-2][0-9])?[0-9][0-9]"
date2 = r"([0-9]{1,3}-)?[0-9]{1,3}[\./][0-9]{1,3}[\./]([1-2][0-9])?[0-9][0-9]"
num = r"[+-]?[0-9]+[0-9/-]*[\.]?[0-9]+|[0-9]+%{0,1}"
url = r"[a-z]+://\S+"
email = r".+@.+\..+"
punc = r"[,;:\-&!\?\.\]/)'`\"\*\+=_~}\[('`\"{/\\\<\>#]"
bad_punc = r"[\'\"]"
bom = r"\xef\xbb\xbf|\ufeff|\u200e"
other = r"\xa0|\xe2?\x80\xa2?[[^׳-׳×a-zA-Z0-9!\?\.,:;\-()\[\]{}]+"
whitespace = r"\s+"
linebreaks = r"{3,}|".join(['\\' + x for x in ['*', '_', '.', '\\', '!', '+', '>', '<', '#', '^', '~', '=', '-']]) + '\n'
repeated = r"\S*(.)\1{3,}\S*"

patterns = [
    (whitespace, None),
    (linebreaks, None),
    (repeated, None),
    (bom, None),
    (date1, 'DATE'),
    (date2, 'DATE'),
    (hour, 'HOUR'),
    (num, 'NUM'),
    (url, 'URL'),
    (punc, 'PUNC'),
    (eng, 'ENG')]

if PYTHON_VERSION_LESS_THAN_3:
    patterns += [(heb.decode('utf-8'), 'HEB')]

patterns += [
    (heb, 'HEB'),
    (other, 'OTHER')]

scanner = Scanner(patterns)


def tokenize(text):
    return scanner.scan(text)
