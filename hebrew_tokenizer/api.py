#!/usr/bin/env python
# encoding: utf-8
import sys

from hebrew_tokenizer.tokenizer import Tokenizer
from hebrew_tokenizer.lexicon import get_lexicon
from hebrew_tokenizer.groups import Groups

PYTHON_VERSION = sys.version_info.major
PYTHON_VERSION_LESS_THAN_3 = PYTHON_VERSION < 3

lexicon = get_lexicon(PYTHON_VERSION_LESS_THAN_3)
tokenizer = Tokenizer(lexicon, Groups, python_version_less_than_3=PYTHON_VERSION_LESS_THAN_3)

def tokenize(text, with_whitespaces=False):
    tokenizer.with_whitespaces = with_whitespaces
    return tokenizer.tokenize(text)


if __name__ == '__main__':
    sent = 'aspirin   aaaaaa  aaaaaaaaaaa —–  dipyridamole'
    sent_tokens = tokenize(sent)
    for st in sent_tokens:
        print(st)

