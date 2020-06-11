#!/usr/bin/env python
# encoding: utf-8
import unittest
from hebrew_tokenizer import tokenize
from hebrew_tokenizer.groups import Groups


def compare(test_name, sentences, tokenization_ground_truth, print_results=False, with_whitespaces=False):
    for n, (s, s_ground_truth) in enumerate(zip(sentences, tokenization_ground_truth)):
        s_tokens = [(t, grp) for grp, t, _, _ in tokenize(s, with_whitespaces=with_whitespaces)]

        if print_results:
            print('\n{test_name} test#{n}'.format(test_name=test_name, n=n+1))
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
    s1_gt = [(u'לדוגמא', Groups.Hebrew), (u',', Groups.Punctuation), (u'ניסיון', Groups.Hebrew), 
             (u'להדיח', Groups.Hebrew), (u'את', Groups.Hebrew), (u'ח"כ', Groups.Hebrew), 
             (u'השכל', Groups.Hebrew), (u'בשל', Groups.Hebrew), (u'חוק', Groups.Hebrew), 
             (u'המרכולים', Groups.Hebrew)]

    s2 = u'אנשים שהולכים בשבת בבוקר לבית הכנסת ובצהריים יושבים בבית קפה. נקודה'
    s2_gt = [(u'אנשים', Groups.Hebrew), (u'שהולכים', Groups.Hebrew), (u'בשבת', Groups.Hebrew), 
             (u'בבוקר', Groups.Hebrew), (u'לבית', Groups.Hebrew), (u'הכנסת', Groups.Hebrew), 
             (u'ובצהריים', Groups.Hebrew), (u'יושבים', Groups.Hebrew), (u'בבית', Groups.Hebrew), 
             (u'קפה', Groups.Hebrew), (u'.', Groups.Punctuation), (u'נקודה', Groups.Hebrew)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Hebrew', sentences, tokenization_ground_truth, print_results)


def hebrew_and_english(print_results=False):
    s1 = u'עמרי כספי נשלח מקבוצתו Golden State Warriors לקבוצת Minnesota Timberwolfs'
    s1_gt = [(u'עמרי', Groups.Hebrew), (u'כספי', Groups.Hebrew), (u'נשלח', Groups.Hebrew), 
             (u'מקבוצתו', Groups.Hebrew), (u'Golden', Groups.English), (u'State', Groups.English), 
             (u'Warriors', Groups.English), (u'לקבוצת', Groups.Hebrew), (u'Minnesota', Groups.English),
             (u'Timberwolfs', Groups.English)]

    s2 = u'לחשוב - Never tried that before.'
    s2_gt = [(u'לחשוב', Groups.Hebrew), (u'-', Groups.Punctuation), (u'Never', Groups.English), (u'tried', Groups.English), (u'that', Groups.English),
             (u'before', Groups.English), (u'.', Groups.Punctuation)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Hebrew and English', sentences, tokenization_ground_truth, print_results)


def hebrew_and_numbers(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי עם אמא למכולת'
    s1_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'5', Groups.Number), (u'אחה"צ', Groups.Hebrew), (u',', Groups.Punctuation),
             (u'יצאתי', Groups.Hebrew), (u'עם', Groups.Hebrew), (u'אמא', Groups.Hebrew), (u'למכולת', Groups.Hebrew)]

    s2 = u' אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15.'
    s2_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'17:00', Groups.Hour), (u'אבל', Groups.Hebrew),
             (u'17', Groups.Number), (u':', Groups.Punctuation), (u'90', Groups.Number), (u'זו', Groups.Hebrew),
             (u'לא', Groups.Hebrew), (u'שעה', Groups.Hebrew), (u'ו', Groups.Hebrew), (u'17:15', Groups.Hour), (u'.', Groups.Punctuation)]

    s3 = u' אני הכי אוהב לאכול קוטג 2.5% של תנובה.'
    s3_gt = [(u'אני', Groups.Hebrew), (u'הכי', Groups.Hebrew), (u'אוהב', Groups.Hebrew), (u'לאכול', Groups.Hebrew), (u'קוטג', Groups.Hebrew),
             (u'2.5%', Groups.Number),  (u'של', Groups.Hebrew), (u'תנובה', Groups.Hebrew), (u'.', Groups.Punctuation)]

    sentences = [s1, s2, s3]
    tokenization_ground_truth = [s1_gt, s2_gt, s3_gt]
    return compare('Hebrew and Numbers', sentences, tokenization_ground_truth, print_results)


def drop_line(print_results=False):
    s1 = u'אתמול ב5 אחה"צ,\n יצאתי עם אמא למכולת'
    s1_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'5', Groups.Number), 
             (u'אחה"צ', Groups.Hebrew), (u',', Groups.Punctuation), (u'יצאתי', Groups.Hebrew), 
             (u'עם', Groups.Hebrew), (u'אמא', Groups.Hebrew), (u'למכולת', Groups.Hebrew)]

    s2 = u' אתמול ב17:00 אבל 17:90 #################################זו לא שעה ו17:15.'
    s2_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'17:00', Groups.Hour), (u'אבל', Groups.Hebrew),
             (u'17', Groups.Number), (u':', Groups.Punctuation), (u'90', Groups.Number), (u'זו', Groups.Hebrew),
             (u'לא', Groups.Hebrew), (u'שעה', Groups.Hebrew), (u'ו', Groups.Hebrew), (u'17:15', Groups.Hour), 
             (u'.', Groups.Punctuation)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Drop Line', sentences, tokenization_ground_truth, print_results)


def repeated_letters(print_results=False):
    s1 = u'אתמול ב5 אחה"צ, יצאתי גגגגגגגגגגגגגגגגג עם אמא למכולת'
    s1_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'5', Groups.Number), (u'אחה"צ', Groups.Hebrew), 
             (u',', Groups.Punctuation), (u'יצאתי', Groups.Hebrew), (u'עם', Groups.Hebrew), (u'אמא', Groups.Hebrew), 
             (u'למכולת', Groups.Hebrew)]

    s2 = u' אתמול ב17:00 אבל 17:90 זו לא שעה ו17:15. NNNNNNNNNNNNNNNNNNNNN'
    s2_gt = [(u'אתמול', Groups.Hebrew), (u'ב', Groups.Hebrew), (u'17:00', Groups.Hour), (u'אבל', Groups.Hebrew),
             (u'17', Groups.Number), (u':', Groups.Punctuation), (u'90', Groups.Number), (u'זו', Groups.Hebrew),
             (u'לא', Groups.Hebrew), (u'שעה', Groups.Hebrew), (u'ו', Groups.Hebrew), (u'17:15', Groups.Hour), 
             (u'.', Groups.Punctuation)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Repeated Letters', sentences, tokenization_ground_truth, print_results)


def quotation_mark(print_results=False):
    s1 = u'אני מודד אורך בס"מ ונפח בסמ"ק'
    s1_gt = [(u'אני', Groups.Hebrew), (u'מודד', Groups.Hebrew), (u'אורך', Groups.Hebrew), (u'בס"מ', Groups.Hebrew),
             (u'ונפח', Groups.Hebrew), (u'בסמ"ק', Groups.Hebrew)]

    s2 = u'i don\'t know and i can\'t tell'
    s2_gt = [(u'i', Groups.English), (u'don\'t', Groups.English), (u'know', Groups.English), (u'and', Groups.English),
             (u'i', Groups.English), (u'can\'t', Groups.English), (u'tell', Groups.English)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Quotation_mark', sentences, tokenization_ground_truth, print_results)


def whitespace(print_results=False):
    s1 = u'אני מודד אורך בס"מ ונפח בסמ"ק.'
    s1_gt = [(u'אני', Groups.Hebrew), (u' ', Groups.Whitespace), (u'מודד', Groups.Hebrew), (u' ', Groups.Whitespace), 
             (u'אורך', Groups.Hebrew), (u' ', Groups.Whitespace), (u'בס"מ', Groups.Hebrew), (u' ', Groups.Whitespace), 
             (u'ונפח', Groups.Hebrew), (u' ', Groups.Whitespace), (u'בסמ"ק', Groups.Hebrew), (u'.', Groups.Punctuation)]

    s2 = u'לחשוב - Never tried that before.'
    s2_gt = [(u'לחשוב', Groups.Hebrew), (u' ', Groups.Whitespace), (u'-', Groups.Punctuation), (u' ', Groups.Whitespace), 
             (u'Never', Groups.English), (u' ', Groups.Whitespace), (u'tried', Groups.English), (u' ', Groups.Whitespace), 
             (u'that', Groups.English), (u' ', Groups.Whitespace), (u'before', Groups.English), (u'.', Groups.Punctuation)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Whitespace', sentences, tokenization_ground_truth, print_results, with_whitespaces=True)


def abbreviations(print_results=False):
    s1 = u'He went to see the E.N.T'
    s1_gt = [(u'He', Groups.English), (u'went', Groups.English), (u'to', Groups.English), (u'see', Groups.English),
             (u'the', Groups.English), (u'E.N.T', Groups.English)]
    s2 = u'e.g, I can eat a gallon of ice cream.'
    s2_gt = [(u'e.g', Groups.English), (u',', Groups.Punctuation), (u'I', Groups.English), (u'can', Groups.English),
             (u'eat', Groups.English), (u'a', Groups.English), (u'gallon', Groups.English), (u'of', Groups.English),
             (u'ice', Groups.English), (u'cream', Groups.English), (u'.', Groups.Punctuation)]

    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Abbreviations', sentences, tokenization_ground_truth, print_results, with_whitespaces=False)


def dash(print_results=False):
    s1 = u'אני רוצה לבדוק עברית-מודרנית'
    s1_gt = [(u'אני', Groups.Hebrew), (u'רוצה', Groups.Hebrew), (u'לבדוק', Groups.Hebrew), 
             (u'עברית', Groups.Hebrew), (u'-', Groups.Punctuation), (u'מודרנית', Groups.Hebrew)]

    s2 = u'מערבית־מודרנית'
    s2_gt = [(u'מערבית', Groups.Hebrew), (u'־', Groups.Punctuation), (u'מודרנית', Groups.Hebrew)]
    sentences = [s1, s2]
    tokenization_ground_truth = [s1_gt, s2_gt]
    return compare('Dash', sentences, tokenization_ground_truth, print_results, with_whitespaces=False)


class Test(unittest.TestCase):
    tests = {'A. Hebrew': hebrew,
             'B. English': hebrew_and_english,
             'C. Numbers_Dates_Hours': hebrew_and_numbers,
             'D. Drop_Line': drop_line,
             'E. Repeated Letters': repeated_letters,
             'F. Quotation_mark': quotation_mark,
             'G. White_Space': whitespace,
             'H. Abbreviations': abbreviations,
             'I. Dash': dash}

    def test_tokenizer(self):
        tests_results = {}
        for test_name, test_func in sorted(self.tests.items()):
            result = test_func(print_results=True)
            tests_results[test_name] = result
            print('\n{test_name:25s} {test_results}\n{line_breaker}'
                  .format(test_name=test_name, test_results=result.__str__(), line_breaker="-"*50))
        assert all(tests_results.values()), 'One of the tests failed'

if __name__ == '__main__':
    unittest.main()