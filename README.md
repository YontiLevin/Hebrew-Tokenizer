[![PyPI download total](https://img.shields.io/pypi/dm/hebrew-tokenizer.svg)](https://pypi.python.org/pypi/hebrew-tokenizer/)  [![PyPI version fury.io](https://badge.fury.io/py/hebrew-tokenizer.svg)](https://pypi.python.org/pypi/hebrew-tokenizer/)
 [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) 


# Hebrew Tokenizer
A very simple python tokenizer for Hebrew text.  
No batteries included - No dependencies needed!

### UPDATES
#### 23/10/21
Hebrew accents/punctuation(ניקוד) support added.

#### 28/04/21
accented letters support was added - great work [Daniel](https://github.com/Gilthans) 👊

#### 23/10/2020
Added support for Python 3.8+.   
The Code look like shit now BUT it's working:smile:.   
In the near future I will wrap it up nicely.  

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

>>> HEBREW, 'אתמול'
>>> PUNCTUATION, ',' 
>>> DATE, '8.6.2018'
>>> PUNCTUATION, ',' 
>>> HEBREW, 'בשעה'
>>> HOUR, '17:00'
>>> HEBREW, 'הלכתי'
>>> HEBREW, 'עם'
>>> HEBREW, 'אמא'
>>> HEBREW, 'למכולת'

# by default it doesn't return whitespaces but it can be done easily
tokens = ht.tokenize(hebrew_text, with_whitespaces=True)  # notice the with_whitespace flag
for grp, token, token_num, (start_index, end_index) in tokens:
    print('{}, {}'.format(grp, token))
  
>>> HEBREW, 'אתמול'
>>> WHITESPACE, ''
>>> PUNCTUATION, ',' 
>>> WHITESPACE, ''
>>> DATE, '8.6.2018'
>>> PUNCTUATION, ','
>>> WHITESPACE, ''
>>> HEBREW, 'בשעה'
>>> WHITESPACE, ''
>>> HOUR, '17:00'
>>> WHITESPACE, ''
>>> HEBREW, 'הלכתי'
>>> WHITESPACE, ''
>>> HEBREW, 'עם'
>>> WHITESPACE, ''
>>> HEBREW, 'אמא'
>>> WHITESPACE, ''
>>> HEBREW, 'למכולת'
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
