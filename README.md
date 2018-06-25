# Hebrew Tokenizer
A very simple python tokenizer for Hebrew text.  
No batteries included - No dependencies needed!

### Usage
```python
import hebtok
hebrew_text = "אתמול, 8.6.2018, בשעה 17:00 הלכתי עם אמא למכולת"
tokens = hebtok.tokenize(text)  # tokenize returns a generator! 
for token in tokens:
  print(token)

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
```

### Installation
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
