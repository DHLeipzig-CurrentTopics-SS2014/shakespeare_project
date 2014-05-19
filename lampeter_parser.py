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