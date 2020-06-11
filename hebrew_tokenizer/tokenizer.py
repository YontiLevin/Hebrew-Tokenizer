from sre_constants import BRANCH, SUBPATTERN
from sre_compile import compile as sre_compile
from sre_parse import Pattern, SubPattern, parse


class Tokenizer:
    def __init__(self, lexicon, group_names, flags=0, with_whitespaces=False, python_version_less_than_3=False):
        self.lexicon = []
        p = []
        s = Pattern()
        s.flags = flags
        if python_version_less_than_3:
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



