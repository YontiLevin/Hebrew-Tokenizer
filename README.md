# Hebrew Tokenizer
A very simple python tokenizer for Hebrew text.  
No batteries included - No dependencies needed!

### Usage
```python
import hebrew_tokenizer as ht
hebrew_text = "אתמול, 8.6.2018, בשעה 17:00 הלכתי עם אמא למכולת"
tokens = ht.tokenize(text)  # tokenize returns a generator!
for grp, token, token_num, (start_index, end_index) in tokens:
  print(grp, token)

>>> (HEB, 'אתמול')
>>> (PUNC, ',' )
>>> (DATE, '8.6.2018')
>>> (PUNC, ',' )
>>> (HEB, 'בשעה')
>>> (HOUR, '17:00')
>>> (HEB, 'הלכתי')
>>> (HEB, 'עם')
>>> (HEB, 'אמא')
>>> (HEB, 'למכולת')

# by default it doesn't return whitespaces but it can be done easily
tokens = ht.tokenize(text, with_whitespaces=True)  # notice the with_whitespace flag
for grp, token, token_num, (start_index, end_index) in tokens:
  print(grp, token)

>>> (HEB, 'אתמול')
>>> (PUNC, ',' )
>>> (WS, ' ')
>>> (DATE, '8.6.2018')
>>> (PUNC, ',' )
>>> (WS, ' ')
>>> (HEB, 'בשעה')
>>> (WS, ' ')
>>> (HOUR, '17:00')
>>> (WS, ' ')
>>> (HEB, 'הלכתי')
>>> (WS, ' ')
>>> (HEB, 'עם')
>>> (WS, ' ')
>>> (HEB, 'אמא')
>>> (WS, ' ')
>>> (HEB, 'למכולת')
```

### Installation
1. via pip
    1. at the moment the project sits at https://test.pypi.org/project/hebrew-tokenizer/
    2. ```pip install -i https://test.pypi.org/simple/ hebrew-tokenizer```
2. from source
    1. Download / Clone
    2. ```python setup.py install```

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
