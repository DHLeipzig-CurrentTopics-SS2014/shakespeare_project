import os, re
from corpora.models import Author, Text, Corpus, Word
from stemming_lib.stemming.porter2 import stem as porter2

# als stemmer porter2

class CorpusParser():

    def parse_folder(self, foldername, corpus_name):
        corpus = Corpus.objects.get_or_create(name=corpus_name)[0]
        for filename in os.listdir(foldername):
            path = ''.join([foldername, filename])
            f = open( path, 'r', encoding='utf-8').read()
            build_text(f, corpus)
            

def build_text(text, corpus):
    author = Author.objects.get_or_create(name=find_author(f))[0]
    text = Text.objects.create(title = find_title(f), author = author, year = find_year(f), text = find_text(f), corpus = corpus)
    wordlist = make_wordlist(text)
    for word in wordlist:
        Word.objects.create(word = word, stemmed = stem_word_porter2(word), text = text)
    
def make_wordlist(text):
# remove everything that is not actually a word (everyting not in a-z and A-Z)
    return re.sub(r'[^a-zA-Z\s]', ' ', text).split()
    
def stem_word_porter2(word):
    return porter2(word)
    
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
