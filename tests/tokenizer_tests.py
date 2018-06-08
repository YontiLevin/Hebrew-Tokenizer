#!/usr/bin/env python
# encoding: utf-8
import unittest
from hebtok import tokenize


def compare(test_name, sentences, tokenization_ground_truth, print_results=False):
    for n, (s, s_ground_truth) in enumerate(zip(sentences, tokenization_ground_truth)):
        s_tokens = [(t, grp) for grp, t, _, _ in tokenize(s)]

        if print_results:
            print('\n{test_name} test #{n}'.format(test_name=test_name, n=n))
            for t, gt in zip(s_tokens, s_ground_truth):
                res = (u'!=', u'X') if t[1] != gt[1] or t[0] != gt[0] else (u'==', u'\N{check mark}')
                print(u'{}({}) {}({}) {}'.format(t[0], t[1], res[0], gt[0], gt[1], res[1]))
        if not len(s_tokens) == len(s_ground_truth):
            return False
        if not all(t == gt for t, gt in zip(s_tokens, s_ground_truth)):
            return False

    return True


def hebrew(print_results=False):
    s1 = u'לדוגמא, ניסיון להדיח את ח"כ השכל בשל חוק המרכולים'
    s1_gt = [(u'לדוגמא', u'HEB'), (u',', u'PUNC'), (u'ניסיון', u'HEB'), (u'להדיח', u'HEB'), (u'את', u'HEB'),
             (u'ח"כ', u'HEB'), (u'השכל', u'HEB'), (u'בשל', u'HEB'), (u'חוק', u'HEB'), (u'המרכולים', u'HEB')]

    s2 = u'אנשים שהולכים בשבת בבוקר לבית הכנסת ובצהריים יושבים בבית קפה. נקודה'
    s2_gt = [(u'אנשים', u'HEB'), (u'שהולכים', u'HEB'), (u'בשבת', u'HEB'), (u'בבוקר', u'HEB'), (u'לבית', u'HEB'),
             (u'הכנסת', u'HEB'), (u'ובצהריים', u'HEB'), (u'יושבים', u'HEB'), (u'בבית', u'HEB'), (u'קפה', u'HEB'),
             (u'.', u'PUNC'), (u'נקודה', u'HEB')]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Hebrew', sentences, tokenization_ground_truth, print_results)


def hebrew_and_english(print_results=False):
    s1 = u'עמרי כספי נשלח מקבוצתו Golden State Warriors לקבוצת Minnesota Timberwolfs'
    s1_gt = [(u'עמרי', u'HEB'), (u'כספי', u'HEB'), (u'נשלח', u'HEB'), (u'מקבוצתו', u'HEB'), (u'Golden', u'ENG'),
             (u'State', u'ENG'), (u'Warriors', u'ENG'), (u'לקבוצת', u'HEB'), (u'Minnesota', u'ENG'),
             (u'Timberwolfs', u'ENG')]

    s2 = u'לחשוב - Never tried that before.'
    s2_gt = [(u'לחשוב', u'HEB'), (u'-', u'PUNC'), (u'Never', u'ENG'), (u'tried', u'ENG'), (u'that', u'ENG'),
             (u'before', u'ENG'), (u'.', u'PUNC')]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Hebrew and English', sentences, tokenization_ground_truth, print_results)


def hebrew_and_numbers(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי עם אמא למכולת'
    s1_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'5', u'NUM'), (u'אחה"צ', u'HEB'), (u',', u'PUNC'),
             (u'יצאתי', u'HEB'), (u'עם', u'HEB'), (u'אמא', u'HEB'), (u'למכולת', u'HEB')]

    s2 = u' אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15.'
    s2_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'17:00', u'HOUR'), (u'אבל', u'HEB'),
             (u'17', u'NUM'), (u':', u'PUNC'), (u'90', u'NUM'), (u'זו', u'HEB'),
             (u'לא', u'HEB'), (u'שעה', u'HEB'), (u'ו', u'HEB'), (u'17:15', u'HOUR'), (u'.', u'PUNC')]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Hebrew and English', sentences, tokenization_ground_truth, print_results)


def drop_line(print_results=False):
    s1 = u'אתמול ב5 אחה"צ,\n יצאתי עם אמא למכולת'
    s1_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'5', u'NUM'), (u'אחה"צ', u'HEB'), (u',', u'PUNC'),
             (u'יצאתי', u'HEB'), (u'עם', u'HEB'), (u'אמא', u'HEB'), (u'למכולת', u'HEB')]

    s2 = u' אתמול ב17:00 אבל 17:90 #################################זו לא שעה ו17:15.'
    s2_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'17:00', u'HOUR'), (u'אבל', u'HEB'),
             (u'17', u'NUM'), (u':', u'PUNC'), (u'90', u'NUM'), (u'זו', u'HEB'),
             (u'לא', u'HEB'), (u'שעה', u'HEB'), (u'ו', u'HEB'), (u'17:15', u'HOUR'), (u'.', u'PUNC')]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Drop Line', sentences, tokenization_ground_truth, print_results)


def repeated_letters(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי גגגגגגגגגגגגגגגגג עם אמא למכולת'
    s1_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'5', u'NUM'), (u'אחה"צ', u'HEB'), (u',', u'PUNC'),
             (u'יצאתי', u'HEB'), (u'עם', u'HEB'), (u'אמא', u'HEB'), (u'למכולת', u'HEB')]

    s2 = u' אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15. NNNNNNNNNNNNNNNNNNNNN'
    s2_gt = [(u'אתמול', u'HEB'), (u'ב', u'HEB'), (u'17:00', u'HOUR'), (u'אבל', u'HEB'),
             (u'17', u'NUM'), (u':', u'PUNC'), (u'90', u'NUM'), (u'זו', u'HEB'),
             (u'לא', u'HEB'), (u'שעה', u'HEB'), (u'ו', u'HEB'), (u'17:15', u'HOUR'), (u'.', u'PUNC')]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Repeated Letters', sentences, tokenization_ground_truth, print_results)


class Test(unittest.TestCase):
    tests = {'A. Hebrew': hebrew,
             'B. English': hebrew_and_english,
             'C. Numbers_Dates_Hours': hebrew_and_numbers,
             'D. Drop_Line': drop_line,
             'E. Repeated Letters': repeated_letters}

    def test_tokenizer(self):
        tests_results = {}
        for test_name, test_func in sorted(self.tests.items()):
            result = test_func(print_results=False)
            tests_results[test_name] = result
            print('{test_name:25s} {test_results}'
                  .format(test_name=test_name, test_results=result.__str__()))
        assert all(tests_results.values()), 'One of the tests failed'

