import os, re
from corpora.models import Author, Text


# als stemmer porter2

class CorpusParser():

    def parse_folder(self, foldername):
        for filename in os.listdir(foldername):
            path = ''.join([foldername, filename])
            f = open( path, 'r', encoding='utf-8').read()
            author = Author.objects.get_or_create(name=find_author(f))[0]
            text = Text.objects.create(title= find_title(f), author=author, year= find_year(f), text=find_text(f))

def find_title(content):
    pattern = re.compile('(<title>)([^<]*)(</title>)', re.IGNORECASE)
    return pattern.search(content).groups()[1]

def find_author(content):
    pattern = re.compile('(<author>)([^<]*)(</author>)', re.IGNORECASE)
    result = pattern.search(content)
    if result == None:
        return 'unknown'
    else:
       return result.groups()[1]

def find_year(content):
    pattern = re.compile('(<year>)([^<]*)(</year>)', re.IGNORECASE)
    return pattern.search(content).groups()[1]

def find_text(content):
    pattern = re.compile('(<text>)(.*)(</text>)', re.IGNORECASE | re.DOTALL)
    return pattern.search(content).groups()[1]
