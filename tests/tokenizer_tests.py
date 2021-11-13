#!/usr/bin/env python
# encoding: utf-8
import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))

import unittest
from hebrew_tokenizer import tokenize
from hebrew_tokenizer.groups import Groups


def compare(
    test_name,
    sentences,
    tokenization_ground_truth,
    print_results=False,
    with_whitespaces=False,
):
    for n, (s, s_ground_truth) in enumerate(zip(sentences, tokenization_ground_truth)):
        s_tokens = [
            (t, grp) for grp, t, _, _ in tokenize(s, with_whitespaces=with_whitespaces)
        ]

        if print_results:
            print("\n{test_name} test#{n}".format(test_name=test_name, n=n + 1))
            for t, gt in zip(s_tokens, s_ground_truth):
                res = (
                    (u"!=", u"X")
                    if t[1] != gt[1] or t[0] != gt[0]
                    else (u"==", u"\N{check mark}")
                )
                print(
                    u"{}({}) {}({}) {}".format(t[0], t[1], res[0], gt[0], gt[1], res[1])
                )
        if not len(s_tokens) == len(s_ground_truth):
            return False
        if not all(t == gt for t, gt in zip(s_tokens, s_ground_truth)):
            return False

    return True


def hebrew(print_results=False):
    s1 = u'לדוגמא, ניסיון להדיח את ח"כ השכל בשל חוק המרכולים'
    s1_gt = [
        (u"לדוגמא", Groups.HEBREW),
        (u",", Groups.PUNCTUATION),
        (u"ניסיון", Groups.HEBREW),
        (u"להדיח", Groups.HEBREW),
        (u"את", Groups.HEBREW),
        (u'ח"כ', Groups.HEBREW),
        (u"השכל", Groups.HEBREW),
        (u"בשל", Groups.HEBREW),
        (u"חוק", Groups.HEBREW),
        (u"המרכולים", Groups.HEBREW),
    ]

    s2 = u"אנשים שהולכים בשבת בבוקר לבית הכנסת ובצהריים יושבים בבית קפה. נקודה"
    s2_gt = [
        (u"אנשים", Groups.HEBREW),
        (u"שהולכים", Groups.HEBREW),
        (u"בשבת", Groups.HEBREW),
        (u"בבוקר", Groups.HEBREW),
        (u"לבית", Groups.HEBREW),
        (u"הכנסת", Groups.HEBREW),
        (u"ובצהריים", Groups.HEBREW),
        (u"יושבים", Groups.HEBREW),
        (u"בבית", Groups.HEBREW),
        (u"קפה", Groups.HEBREW),
        (u".", Groups.PUNCTUATION),
        (u"נקודה", Groups.HEBREW),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare("Hebrew", sentences, tokenization_ground_truth, print_results)


def hebrew_and_english(print_results=False):
    s1 = u"עמרי כספי נשלח מקבוצתו Golden State Warriors לקבוצת Minnesota Timberwolfs"
    s1_gt = [
        (u"עמרי", Groups.HEBREW),
        (u"כספי", Groups.HEBREW),
        (u"נשלח", Groups.HEBREW),
        (u"מקבוצתו", Groups.HEBREW),
        (u"Golden", Groups.ENGLISH),
        (u"State", Groups.ENGLISH),
        (u"Warriors", Groups.ENGLISH),
        (u"לקבוצת", Groups.HEBREW),
        (u"Minnesota", Groups.ENGLISH),
        (u"Timberwolfs", Groups.ENGLISH),
    ]

    s2 = u"לחשוב - Never tried that before."
    s2_gt = [
        (u"לחשוב", Groups.HEBREW),
        (u"-", Groups.PUNCTUATION),
        (u"Never", Groups.ENGLISH),
        (u"tried", Groups.ENGLISH),
        (u"that", Groups.ENGLISH),
        (u"before", Groups.ENGLISH),
        (u".", Groups.PUNCTUATION),
    ]

    s3 = u"ביקרתי ב-São Paulo"
    s3_gt = [
        (u"ביקרתי", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"-", Groups.PUNCTUATION),
        (u"São", Groups.ENGLISH),
        (u"Paulo", Groups.ENGLISH),
    ]

    sentences = [s1, s2, s3]
    tokenization_ground_truth = [s1_gt, s2_gt, s3_gt]
    return compare(
        "Hebrew and English", sentences, tokenization_ground_truth, print_results
    )

def hebrew_and_foreign(print_results=True):
    cryllic_MTC = b'\xD0\x9C\xD0\xA2\xD0\xA1'.decode('utf8')
    cryllic_MTC3 = b'\xD0\x9C\xD0\xA2\xD0\xA13'.decode('utf8')
    cryllic_M3TC = b'\xD0\x9C3\xD0\xA2\xD0\xA1'.decode('utf8')
    english_MTC = 'MTC'
    hebrew_MTC = 'מטח'
    s1 = f'{cryllic_MTC} {cryllic_MTC3} {cryllic_M3TC}-{english_MTC} {hebrew_MTC}'
    s1_gt = [
        (cryllic_MTC, Groups.FOREIGN),
        (cryllic_MTC3, Groups.FOREIGN),
        (cryllic_M3TC, Groups.FOREIGN),
        ('-', Groups.PUNCTUATION),
        (english_MTC, Groups.ENGLISH),
        (hebrew_MTC, Groups.HEBREW)
    ]
    return compare(
        "Hebrew and Foreign languages", [s1], [s1_gt], print_results
    )


def hebrew_and_numbers(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי עם אמא למכולת'
    s1_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"5", Groups.NUMBER),
        (u'אחה"צ', Groups.HEBREW),
        (u",", Groups.PUNCTUATION),
        (u"יצאתי", Groups.HEBREW),
        (u"עם", Groups.HEBREW),
        (u"אמא", Groups.HEBREW),
        (u"למכולת", Groups.HEBREW),
    ]

    s2 = u" אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15."
    s2_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"17:00", Groups.HOUR),
        (u"אבל", Groups.HEBREW),
        (u"17", Groups.NUMBER),
        (u":", Groups.PUNCTUATION),
        (u"90", Groups.NUMBER),
        (u"זו", Groups.HEBREW),
        (u"לא", Groups.HEBREW),
        (u"שעה", Groups.HEBREW),
        (u"ו", Groups.HEBREW),
        (u"17:15", Groups.HOUR),
        (u".", Groups.PUNCTUATION),
    ]

    s3 = u" אני הכי אוהב לאכול קוטג 2.5% של תנובה."
    s3_gt = [
        (u"אני", Groups.HEBREW),
        (u"הכי", Groups.HEBREW),
        (u"אוהב", Groups.HEBREW),
        (u"לאכול", Groups.HEBREW),
        (u"קוטג", Groups.HEBREW),
        (u"2.5%", Groups.NUMBER),
        (u"של", Groups.HEBREW),
        (u"תנובה", Groups.HEBREW),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2, s3]
    tokenization_ground_truth = [s1_gt, s2_gt, s3_gt]
    return compare(
        "Hebrew and Numbers", sentences, tokenization_ground_truth, print_results
    )


def drop_line(print_results=False):
    s1 = u'אתמול ב5 אחה"צ,\n יצאתי עם אמא למכולת'
    s1_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"5", Groups.NUMBER),
        (u'אחה"צ', Groups.HEBREW),
        (u",", Groups.PUNCTUATION),
        (u"יצאתי", Groups.HEBREW),
        (u"עם", Groups.HEBREW),
        (u"אמא", Groups.HEBREW),
        (u"למכולת", Groups.HEBREW),
    ]

    s2 = u" אתמול ב17:00 אבל 17:90 #################################זו לא שעה ו17:15."
    s2_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"17:00", Groups.HOUR),
        (u"אבל", Groups.HEBREW),
        (u"17", Groups.NUMBER),
        (u":", Groups.PUNCTUATION),
        (u"90", Groups.NUMBER),
        (u"זו", Groups.HEBREW),
        (u"לא", Groups.HEBREW),
        (u"שעה", Groups.HEBREW),
        (u"ו", Groups.HEBREW),
        (u"17:15", Groups.HOUR),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare("Drop Line", sentences, tokenization_ground_truth, print_results)


def repeated_letters(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי גגגגגגגגגגגגגגגגג עם אמא למכולת'
    s1_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"5", Groups.NUMBER),
        (u'אחה"צ', Groups.HEBREW),
        (u",", Groups.PUNCTUATION),
        (u"יצאתי", Groups.HEBREW),
        (u"עם", Groups.HEBREW),
        (u"אמא", Groups.HEBREW),
        (u"למכולת", Groups.HEBREW),
    ]

    s2 = u" אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15. NNNNNNNNNNNNNNNNNNNNN"
    s2_gt = [
        (u"אתמול", Groups.HEBREW),
        (u"ב", Groups.HEBREW),
        (u"17:00", Groups.HOUR),
        (u"אבל", Groups.HEBREW),
        (u"17", Groups.NUMBER),
        (u":", Groups.PUNCTUATION),
        (u"90", Groups.NUMBER),
        (u"זו", Groups.HEBREW),
        (u"לא", Groups.HEBREW),
        (u"שעה", Groups.HEBREW),
        (u"ו", Groups.HEBREW),
        (u"17:15", Groups.HOUR),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare(
        "Repeated Letters", sentences, tokenization_ground_truth, print_results
    )


def quotation_mark(print_results=False):
    s1 = u'אני מודד אורך בס"מ ונפח בסמ"ק'
    s1_gt = [
        (u"אני", Groups.HEBREW),
        (u"מודד", Groups.HEBREW),
        (u"אורך", Groups.HEBREW),
        (u'בס"מ', Groups.HEBREW),
        (u"ונפח", Groups.HEBREW),
        (u'בסמ"ק', Groups.HEBREW),
    ]

    s2 = u"i don't know and i can't tell"
    s2_gt = [
        (u"i", Groups.ENGLISH),
        (u"don't", Groups.ENGLISH),
        (u"know", Groups.ENGLISH),
        (u"and", Groups.ENGLISH),
        (u"i", Groups.ENGLISH),
        (u"can't", Groups.ENGLISH),
        (u"tell", Groups.ENGLISH),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare(
        "Quotation_mark", sentences, tokenization_ground_truth, print_results
    )


def whitespace(print_results=False):
    s1 = u'אני מודד אורך בס"מ ונפח בסמ"ק.'
    s1_gt = [
        (u"אני", Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u"מודד", Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u"אורך", Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u'בס"מ', Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u"ונפח", Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u'בסמ"ק', Groups.HEBREW),
        (u".", Groups.PUNCTUATION),
    ]

    s2 = u"לחשוב - Never tried that before."
    s2_gt = [
        (u"לחשוב", Groups.HEBREW),
        (u" ", Groups.WHITESPACE),
        (u"-", Groups.PUNCTUATION),
        (u" ", Groups.WHITESPACE),
        (u"Never", Groups.ENGLISH),
        (u" ", Groups.WHITESPACE),
        (u"tried", Groups.ENGLISH),
        (u" ", Groups.WHITESPACE),
        (u"that", Groups.ENGLISH),
        (u" ", Groups.WHITESPACE),
        (u"before", Groups.ENGLISH),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare(
        "Whitespace",
        sentences,
        tokenization_ground_truth,
        print_results,
        with_whitespaces=True,
    )


def abbreviations(print_results=False):
    s1 = u"He went to see the E.N.T"
    s1_gt = [
        (u"He", Groups.ENGLISH),
        (u"went", Groups.ENGLISH),
        (u"to", Groups.ENGLISH),
        (u"see", Groups.ENGLISH),
        (u"the", Groups.ENGLISH),
        (u"E.N.T", Groups.ENGLISH),
    ]
    s2 = u"e.g, I can eat a gallon of ice cream."
    s2_gt = [
        (u"e.g", Groups.ENGLISH),
        (u",", Groups.PUNCTUATION),
        (u"I", Groups.ENGLISH),
        (u"can", Groups.ENGLISH),
        (u"eat", Groups.ENGLISH),
        (u"a", Groups.ENGLISH),
        (u"gallon", Groups.ENGLISH),
        (u"of", Groups.ENGLISH),
        (u"ice", Groups.ENGLISH),
        (u"cream", Groups.ENGLISH),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare(
        "Abbreviations",
        sentences,
        tokenization_ground_truth,
        print_results,
        with_whitespaces=False,
    )


def dash(print_results=False):
    s1 = u"אני רוצה לבדוק עברית-מודרנית"
    s1_gt = [
        (u"אני", Groups.HEBREW),
        (u"רוצה", Groups.HEBREW),
        (u"לבדוק", Groups.HEBREW),
        (u"עברית", Groups.HEBREW),
        (u"-", Groups.PUNCTUATION),
        (u"מודרנית", Groups.HEBREW),
    ]

    s2 = u"מערבית־מודרנית"
    s2_gt = [
        (u"מערבית", Groups.HEBREW),
        (u"־", Groups.PUNCTUATION),
        (u"מודרנית", Groups.HEBREW),
    ]
    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare(
        "Dash",
        sentences,
        tokenization_ground_truth,
        print_results,
        with_whitespaces=False,
    )


def dates(print_results=False):
    s1 = u' אני מודד אורך בס"מ ונפח בסמ"ק בתאריך 10.6.2020.'
    s1_gt = [
        (u"אני", Groups.HEBREW),
        (u"מודד", Groups.HEBREW),
        (u"אורך", Groups.HEBREW),
        (u'בס"מ', Groups.HEBREW),
        (u"ונפח", Groups.HEBREW),
        (u'בסמ"ק', Groups.HEBREW),
        (u"בתאריך", Groups.HEBREW),
        (u"10.6.2020", Groups.DATE),
        (u".", Groups.PUNCTUATION),
    ]

    s2 = u"לחשוב - Never tried that before 10/06/2020."
    s2_gt = [
        (u"לחשוב", Groups.HEBREW),
        (u"-", Groups.PUNCTUATION),
        (u"Never", Groups.ENGLISH),
        (u"tried", Groups.ENGLISH),
        (u"that", Groups.ENGLISH),
        (u"before", Groups.ENGLISH),
        (u"10/06/2020", Groups.DATE),
        (u".", Groups.PUNCTUATION),
    ]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare("Dates", sentences, tokenization_ground_truth, print_results)


def hebrew_accents(print_results=False):
    s1 = u'מָתֵמָטִיקָה זה קשה!'
    s1_gt = [
        (u"מָתֵמָטִיקָה", Groups.HEBREW),
        (u"זה", Groups.HEBREW),
        (u"קשה", Groups.HEBREW),
        (u"!", Groups.PUNCTUATION),
    ]

    sentences = [s1]
    tokenization_ground_truth = [s1_gt]
    return compare("hebrew_accents", sentences, tokenization_ground_truth, print_results)

class Test(unittest.TestCase):
    tests = {
        "A. Hebrew": hebrew,
        "B. English": hebrew_and_english,
        "C. Numbers_Hours": hebrew_and_numbers,
        "D. Drop_Line": drop_line,
        "E. Repeated Letters": repeated_letters,
        "F. Quotation_mark": quotation_mark,
        "G. White_Space": whitespace,
        "H. Abbreviations": abbreviations,
        "I. Dash": dash,
        "J. Dates": dates,
        "K. Hebrew accents": hebrew_accents,
        "L. Hebrew and Foreign": hebrew_and_foreign
    }

    def test_tokenizer(self):
        tests_results = {}
        for test_name, test_func in sorted(self.tests.items()):
            result = test_func(print_results=True)
            tests_results[test_name] = result
            print(
                "\n{test_name:25s} {test_results}\n{line_breaker}".format(
                    test_name=test_name,
                    test_results=result.__str__(),
                    line_breaker="-" * 50,
                )
            )
        assert all(tests_results.values()), "One of the tests failed"


if __name__ == "__main__":
    unittest.main()
