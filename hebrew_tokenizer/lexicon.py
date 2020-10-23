#!/usr/bin/env python
# encoding: utf-8
from sre_constants import GROUPREF
from hebrew_tokenizer.groups import Groups


# patterns
_heb = r"[א-ת]" + "{1,}[']?[\"]*" + "[א-ת]" + "{1,}|" + "[א-ת]"
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
_linebreaks = (
    r"{3,}|".join(
        [
            "\\" + x
            for x in ["*", "_", ".", "\\", "!", "+", ">", "<", "#", "^", "~", "=", "-"]
        ]
    )
    + "\n"
)
_repeated = r"\S*(\S)\1{3,}\S*"
_repeated_for_python_above_3_7 = r"\S*(\S)\4{3,}\S*"


def get_lexicon(python_version_less_than_3=False, python_version_more_than_3_7=False):
    # the expected (pattern, group mapping) format for the tokenizer
    global _repeated

    if python_version_more_than_3_7:
        _repeated = _repeated_for_python_above_3_7

    lexicon = [
        (_whitespace, Groups.WHITESPACE),
        (_linebreaks, Groups.LINEBREAK),
        (_repeated, Groups.REPEATED),
        (_bom, Groups.BOM),
        (_date1, Groups.DATE_1),
        (_date2, Groups.DATE_2),
        (_hour, Groups.HOUR),
        (_num, Groups.NUMBER),
        (_url, Groups.URL),
        (_eng_abbrev, Groups.ENGLISH_1),
        (_punc, Groups.PUNCTUATION),
        (_eng, Groups.ENGLISH_2),
    ]

    if python_version_less_than_3:
        lexicon += [(_heb.decode("utf-8"), Groups.HEBREW_1)]

    lexicon += [(_heb, Groups.HEBREW_2), (_other, Groups.OTHER)]

    if python_version_more_than_3_7:
        lexicon = [(b, a) for a, b in lexicon]

    return lexicon