import os, re
from corpora.models import Author, Text, Corpus, Word, WordInTextCount
from libs.stemming_lib.stemming.porter2 import stem as porter2

class CorpusParser():

    def parse_folder(self, foldername, corpus_name):
        corpus = Corpus.objects.get_or_create(name=corpus_name)[0]
        for filename in os.listdir(foldername):
            path = '/'.join([foldername, filename])
            f = open( path, 'r', encoding='utf-8').read()
            print(filename)
            author = Author.objects.get_or_create(name=find_author(f))[0]
            build_text(find_title(f), find_text(f), corpus, author, find_year(f))
            

def build_text(title, text, corpus, author, year):
    the_text = Text.objects.create(title= title, author = author, year = year, text = text, corpus = corpus)
    print('making wordlist')
    wordlist= make_wordlist(text)
    counted_words = make_count_wordlist(wordlist)
    # make words in wordlist unique
    wordlist = list(set(wordlist))
    existing = get_existing_word_objects(wordlist)
    for word_obj in existing:
        wordlist.remove(word_obj.word)
    # now wordlist only contains words not known in db
    new_words = map(create_word_object, wordlist)
    Word.objects.bulk_create(list(new_words))
    word_in_text_counts = map(create_word_in_text_count_object, counted_words.keys(), counted_words.values(), [the_text]*len(counted_words))
    WordInTextCount.objects.bulk_create(word_in_text_counts)

def create_word_object(word_str):
    return Word(word = word_str, stemmed = stem_word_porter2(word_str))

def create_word_in_text_count_object(word_str, count, text):
    return WordInTextCount(word=Word.objects.get(word=word_str), text = text, count = count)

def get_existing_word_objects(wordlist):
    wordlist= wordlist
    existing = []
    offset = 0
    steplength = 50
    while offset <= len(wordlist):
        existing.extend(Word.objects.filter(word__in=wordlist[offset:offset+steplength]))
        offset += steplength
    return existing
    
def make_count_wordlist(wordlist):
    words = {}
    for word in wordlist:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1
    return words
                
def make_wordlist(text):
    text = text.lower()
# remove everything that is not actually a word (everyting not in a-z and A-Z)
    return re.sub(r'[^a-zäüöß\s]', ' ', text).split()
    
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
