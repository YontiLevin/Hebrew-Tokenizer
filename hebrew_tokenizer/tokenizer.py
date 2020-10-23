import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))

from hebrew_tokenizer.lexicon import get_lexicon
from hebrew_tokenizer.groups import Groups, GroupsReverseMapping

PYTHON_VERSION = sys.version_info.major
PYTHON_SUB_VERSION = sys.version_info.minor
PYTHON_VERSION_LESS_THAN_3 = PYTHON_VERSION < 3
PYTHON_VERSION_MORE_THAN_3_7 = (
    not PYTHON_VERSION_LESS_THAN_3
) and PYTHON_SUB_VERSION > 7
if PYTHON_VERSION_MORE_THAN_3_7:
    import re
else:
    from sre_constants import BRANCH, SUBPATTERN
    from sre_compile import compile as sre_compile
    from sre_parse import Pattern, SubPattern, parse

if not PYTHON_VERSION_MORE_THAN_3_7:

    class Tokenizer:
        def __init__(self, flags=0, with_whitespaces=False):
            self.lexicon = get_lexicon(
                PYTHON_VERSION_LESS_THAN_3, PYTHON_VERSION_MORE_THAN_3_7
            )
            self.groups = Groups

            p = []
            s = Pattern()
            s.flags = flags
            if PYTHON_VERSION_LESS_THAN_3:
                s.groups = len(self.lexicon) + 1
                old_lexicon = get_lexicon(
                    PYTHON_VERSION_LESS_THAN_3, PYTHON_VERSION_MORE_THAN_3_7
                )
                for group, (phrase, name) in enumerate(old_lexicon, 1):
                    p.append(
                        SubPattern(
                            s,
                            [
                                (SUBPATTERN, (group, parse(phrase, flags))),
                            ],
                        )
                    )
                    self.lexicon.append((group - 1, name))
            else:
                for phrase, name in self.lexicon:
                    gid = s.opengroup()
                    p.append(
                        SubPattern(
                            s,
                            [
                                (SUBPATTERN, (gid, 0, 0, parse(phrase, flags))),
                            ],
                        )
                    )
                    s.closegroup(gid, p[-1])

            p = SubPattern(s, [(BRANCH, (None, p))])
            self.scanner = sre_compile(p).scanner
            self.with_whitespaces = with_whitespaces

        def tokenize(self, string):
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
                    grp_name = GroupsReverseMapping[grp_name]
                    end_idx = m.end()

                    if grp_name:
                        if (
                            grp_name == self.groups.WHITESPACE
                            and not self.with_whitespaces
                        ):
                            pass
                        else:
                            _start_idx = start_idx
                            if add_global_idx_flag:
                                _start_idx += global_idx
                            word = string[_start_idx : end_idx + global_idx]
                            yield grp_name, word, token_num, (
                                _start_idx,
                                end_idx + global_idx,
                            )
                            token_num += 1

                    start_idx = end_idx
                    add_global_idx_flag = True

                if end_idx < global_idx:
                    start_idx += global_idx
                if start_idx >= string_len:
                    break
                end_idx = start_idx + 1
                unknown_token = string[start_idx:end_idx]
                yield "UNKNOWN", unknown_token, token_num, (start_idx, end_idx)
                token_num += 1
                start_idx = end_idx
                global_idx = start_idx


else:

    class Tokenizer:
        def __init__(self, with_whitespaces=False):
            self.lexicon = get_lexicon(
                PYTHON_VERSION_LESS_THAN_3, PYTHON_VERSION_MORE_THAN_3_7
            )
            self.groups = Groups

            self.scanner = re.compile(
                "|".join(
                    "(?P<{grp}>{reg})".format(grp=grp, reg=reg)
                    for (grp, reg) in self.lexicon
                )
            )

            self.with_whitespaces = with_whitespaces

        def tokenize(self, string):
            global_idx, start_idx, end_idx = 0, 0, 0
            line_start, token_num = 0, 0
            string_len = len(string)
            while start_idx < string_len:
                add_global_idx_flag = False
                string = string[start_idx:]
                for match in self.scanner.finditer(string):
                    grp_name = GroupsReverseMapping[match.lastgroup]
                    start_idx, end_idx = match.span()

                    if grp_name:
                        if (
                            grp_name == self.groups.WHITESPACE
                            and not self.with_whitespaces
                        ):
                            pass
                        else:
                            _start_idx = start_idx
                            if add_global_idx_flag:
                                _start_idx += global_idx
                            word = string[_start_idx : end_idx + global_idx]
                            yield grp_name, word, token_num, (
                                _start_idx,
                                end_idx + global_idx,
                            )
                            token_num += 1

                    start_idx = end_idx
                    add_global_idx_flag = True

                if end_idx < global_idx:
                    start_idx += global_idx
                if start_idx >= string_len:
                    break
                end_idx = start_idx + 1
                unknown_token = string[start_idx:end_idx]
                yield "UNKNOWN", unknown_token, token_num, (start_idx, end_idx)
                token_num += 1
                start_idx = end_idx
                global_idx = start_idx


tokenizer = Tokenizer()
