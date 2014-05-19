import re

def find_title(content):
	pattern = re.compile('(<TITLE>)([^<]*)(</TITLE>)', re.IGNORECASE)
	return pattern.search(content).groups()[1]

def find_author(content):
	pattern = re.compile('(<PERSNAME>)([^<]*)(</PERSNAME>)', re.IGNORECASE)
	return pattern.search(content).groups()[1]

def find_date(content):
	pattern = re.compile('(<DATE>)([^<]*)(</DATE>)', re.IGNORECASE)
	return pattern.search(content).groups()[1]

def find_text(content):
	pattern = re.compile('(<body>)(.*)(</body>)', re.IGNORECASE | re.DOTALL)
	return pattern.search(content).groups()[1]

def clean_from_nonletters(text):
    return re.sub(r'[^a-zA-Z\s]', ' ', text)

def clean_from_markup(text):
	pattern = re.compile('<.*?>', re.IGNORECASE | re.DOTALL)
    return pattern.sub('', text)
    
def clean_from_entities(text):
    pattern = re.compile('&[a-zA-Z]{1,5};', re.IGNORECASE)
    return pattern.sub('', text)

# Text ist im <TEXT> tag enthalten
# bereinigen von tags und entities (&rehy;, <RO>, <P>, <NOTE>, jede menge anderes)
# danach alle satzzeichen und zahlen entfernen
# split
# durchzählen und wörter mit nummern schreiben
