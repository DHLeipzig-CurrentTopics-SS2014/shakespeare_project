import os, re
from corpora.models import Author, Text, Corpus, Word
from libs.stemming_lib.stemming.porter2 import stem as porter2

class CorpusParser():

    def parse_folder(self, foldername, corpus_name):
        corpus = Corpus.objects.get_or_create(name=corpus_name)[0]
        for filename in os.listdir(foldername):
            path = '/'.join([foldername, filename])
            f = open( path, 'r', encoding='utf-8').read()
            print(filename)
            build_text(f, corpus)
            

def build_text(text, corpus):
    author = Author.objects.get_or_create(name=find_author(text))[0]
    the_text = Text.objects.create(title = find_title(text), author = author, year = find_year(text), text = find_text(text), corpus = corpus)
    print('making wordlist')
    wordlist = make_wordlist(text)
    words=[]
    for word in wordlist:
        words.append(Word(word = word, stemmed = stem_word_porter2(word), text = the_text))
    Word.objects.bulk_create(words)
    
def make_wordlist(text):
# remove everything that is not actually a word (everyting not in a-z and A-Z)
    return re.sub(r'[^a-zA-ZäüöÄÜÖß\s]', ' ', text).split()
    
def stem_word_porter2(word):
    return porter2(word)
    
def find_author(content):
    pattern = re.compile('(<author>)([^<]*)(</author>)', re.IGNORECASE)
    result = pattern.search(content)
    if result == None:
        return 'unknown'
    else:
       return result.groups()[1]

def find_title(content):
    return find_tag_content('title', content)

def find_year(content):
    return find_tag_content('year', content)

def find_tag_content(tag, xmltext):
    pattern = re.compile('(<{0}>)([^<]*)(</{0}>)'.format(tag), re.IGNORECASE)
    return pattern.search(xmltext).groups()[1]

def find_text(content):
    pattern = re.compile('(<text>)(.*)(</text>)', re.IGNORECASE | re.DOTALL)
    return pattern.search(content).groups()[1]
