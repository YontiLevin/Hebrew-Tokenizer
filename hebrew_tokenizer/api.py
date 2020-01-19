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
    def __init__(self, lexicon, group_names, flags=0, with_whitespaces=False):
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
        self.with_whitespaces = with_whitespaces
        self.group_names = group_names

    def scan(self, string):
        global_idx, start_idx, end_idx = 0, 0, 0
        token_num = 0
        breakaway_counter = 0
        string_len = len(string)
        while start_idx < string_len:
            add_global_idx_flag = False
            match = self.scanner(string[start_idx:]).match
            matches = [m for m in iter(match, None)]
            for m in matches:
                grp_name = self.lexicon[m.lastindex - 1][1]
                end_idx = m.end()

                if grp_name:
                    if grp_name == self.group_names.WHITESPACE and not self.with_whitespaces:
                        pass
                    else:
                        _start_idx = start_idx
                        if add_global_idx_flag:
                            _start_idx += global_idx
                        word = string[_start_idx:end_idx+global_idx]
                        yield grp_name, word, token_num, (_start_idx, end_idx+global_idx)
                        token_num += 1

                start_idx = end_idx
                add_global_idx_flag = True

            if end_idx < global_idx:
                start_idx += global_idx
            if start_idx >= string_len:
                break
            end_idx = start_idx+1
            unknown_token = string[start_idx:end_idx]
            yield 'UNKNOWN', unknown_token, token_num, (start_idx, end_idx)
            token_num += 1
            start_idx = end_idx
            global_idx = start_idx


# patterns
_heb = r"[א-ת]" + "{1,}[\']?[\"]*" + "[א-ת]" + "{1,}|" + "[א-ת]"
_eng = r"[a-zA-Z]{1,}[\']?[\"]*[a-zA-Z0-9]{1,}|[a-zA-Z][a-zA-Z0-9]*"
_eng_abbrev = r"[a-zA-Z]{1}\.[a-zA-Z]{1}(\.[a-zA-Z]){0,1}"
_hour = r"[0-2]?[0-9]:[0-5][0-9]"
_date1 = r"[0-9]{1,3}-[0-9]{1,3}-([1-2][0-9])?[0-9][0-9]"
_date2 = r"([0-9]{1,3}-)?[0-9]{1,3}[\./][0-9]{1,3}[\./]([1-2][0-9])?[0-9][0-9]"
_num = r"[+-]?([0-9]+[0-9/-]*[\.]?[0-9]+|[0-9]+)%{0,1}"
_url = r"[a-z]+://\S+"
_email = r".+@.+\..+"
_punc = r"[,;:\-&!\?\.\]/)'`\"\*\+=_~}\[('`\"{/\\\<\>#%־]"
_bad_punc = r"[\'\"]"
_bom = r"\xef\xbb\xbf|\ufeff|\u200e"
_other = r"\xa0|\xe2?\x80\xa2?[[^׳-׳×a-zA-Z0-9!\?\.,:;\-()\[\]{}]+"
_whitespace = r"\s+"
_linebreaks = r"{3,}|".join(['\\' + x for x in ['*', '_', '.', '\\', '!', '+', '>', '<', '#', '^', '~', '=', '-']]) + '\n'
_repeated = r"\S*(\S)\1{3,}\S*"


# group names
class Groups(object):
    WHITESPACE = 'WS'
    DATE = 'DATE'
    HOUR = 'HOUR'
    NUMBER = 'NUM'
    URL = 'URL'
    PUNCTUATION = 'PUNC'
    ENGLISH = 'ENG'
    HEBREW = 'HEB'
    OTHER = 'OTHER'


# pattern 2 group mapping
patterns = [
    (_whitespace, Groups.WHITESPACE),
    (_linebreaks, None),
    (_repeated, None),
    (_bom, None),
    (_date1, Groups.DATE),
    (_date2, Groups.DATE),
    (_hour, Groups.HOUR),
    (_num, Groups.NUMBER),
    (_url, Groups.URL),
    (_eng_abbrev, Groups.ENGLISH),
    (_punc, Groups.PUNCTUATION),
    (_eng, Groups.ENGLISH)]

if PYTHON_VERSION_LESS_THAN_3:
    patterns += [(_heb.decode('utf-8'), Groups.HEBREW)]

patterns += [
    (_heb, Groups.HEBREW),
    (_other, Groups.OTHER)]


# scanner definition
scanner = Scanner(patterns, Groups)


def tokenize(text, with_whitespaces=False):
    scanner.with_whitespaces = with_whitespaces
    return scanner.scan(text)


if __name__ == '__main__':
    sent = 'aspirin   aaaaaa  aaaaaaaaaaa —–  dipyridamole'
    sent_tokens = tokenize(sent)
    for st in sent_tokens:
        print(st)

