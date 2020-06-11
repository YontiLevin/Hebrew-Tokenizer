#!/usr/bin/env python
# encoding: utf-8
from hebrew_tokenizer.groups import Groups


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
_punc = r"[,;:\-&!\?\.\]/)'`\"\*\+=_~}\[('`\"{/\\\<\>#%־ ֿֿ]"
_bad_punc = r"[\'\"]"
_bom = r"\xef\xbb\xbf|\ufeff|\u200e"
_other = r"\xa0|\xe2?\x80\xa2?[[^׳-׳×a-zA-Z0-9!\?\.,:;\-()\[\]{}]+"
_whitespace = r"\s+"
_linebreaks = r"{3,}|".join(['\\' + x for x in ['*', '_', '.', '\\', '!', '+', '>', '<', '#', '^', '~', '=', '-']]) + '\n'
_repeated = r"\S*(\S)\1{3,}\S*"



def get_lexicon(python_version_less_than_3=False):
    # the expected (pattern, group mapping) format for the tokenizer
    lexicon = [
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

    if python_version_less_than_3:
        lexicon += [(_heb.decode('utf-8'), Groups.HEBREW)]

    lexicon += [
        (_heb, Groups.HEBREW),
        (_other, Groups.OTHER)]

    return lexicon