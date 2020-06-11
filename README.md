[![PyPI download total](https://img.shields.io/pypi/dm/hebrew-tokenizer.svg)](https://pypi.python.org/pypi/hebrew-tokenizer/)  [![PyPI version fury.io](https://badge.fury.io/py/hebrew-tokenizer.svg)](https://pypi.python.org/pypi/hebrew-tokenizer/)
 [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) 


# Hebrew Tokenizer
A very simple python tokenizer for Hebrew text.  
No batteries included - No dependencies needed!

### Installation
1. via pip
    1. ```pip install hebrew_tokenizer```
2. from source
    1. Download / Clone
    2. ```python setup.py install```

### Usage
```python
import hebrew_tokenizer as ht
hebrew_text = "אתמול, 8.6.2018, בשעה 17:00 הלכתי עם אמא למכולת"
tokens = ht.tokenize(hebrew_text)  # tokenize returns a generator!
for grp, token, token_num, (start_index, end_index) in tokens:
    print('{}, {}'.format(grp, token))

>>> Groups.HEBREW, 'אתמול'
>>> Groups.PUNCTUATION, ',' 
>>> Groups.DATE, '8.6.2018'
>>> Groups.PUNCTUATION, ',' 
>>> Groups.HEBREW, 'בשעה'
>>> Groups.HOUR, '17:00'
>>> Groups.HEBREW, 'הלכתי'
>>> Groups.HEBREW, 'עם'
>>> Groups.HEBREW, 'אמא'
>>> Groups.HEBREW, 'למכולת'

# by default it doesn't return whitespaces but it can be done easily
tokens = ht.tokenize(hebrew_text, with_whitespaces=True)  # notice the with_whitespace flag
for grp, token, token_num, (start_index, end_index) in tokens:
    print('{}, {}'.format(grp, token))
  
>>> Groups.HEBREW, 'אתמול'
>>> Groups.WHITESPACE, ''
>>> Groups.PUNCTUATION, ',' 
>>> Groups.WHITESPACE, ''
>>> Groups.DATE, '8.6.2018'
>>> Groups.PUNCTUATION, ','
>>> Groups.WHITESPACE, ''
>>> Groups.HEBREW, 'בשעה'
>>> Groups.WHITESPACE, ''
>>> Groups.HOUR, '17:00'
>>> Groups.WHITESPACE, ''
>>> Groups.HEBREW, 'הלכתי'
>>> Groups.WHITESPACE, ''
>>> Groups.HEBREW, 'עם'
>>> Groups.WHITESPACE, ''
>>> Groups.HEBREW, 'אמא'
>>> Groups.WHITESPACE, ''
>>> Groups.HEBREW, 'למכולת'
```

### Disclaimer
This is __***NOT***__ a POS tagger.   
If that is what you are looking for - check out [yap](https://github.com/habeanf/yap).


### Contribute  
Found a special case where the tokenizer fails?   
1. Try to fix it on your own by improving the regex patterns the tokenizer is based on.  
2. Make sure that your improvement doesn't break the other scenarios in test.py
3. Add you special case to test.py 
4. Commit a pull request.  

### NLPH
For other great Hebrew resources check out [NLPH](https://github.com/NLPH/NLPH_Resources)
