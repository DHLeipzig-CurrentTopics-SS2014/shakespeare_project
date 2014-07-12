import os, re
from corpora.models import Author, Text, Corpus, Word, WordInTextCount
from libs.stemming_lib.stemming.porter2 import stem as porter2

class CorpusParser():
    def parse_files(self, files, corpus_name):
        print(files)
        corpus = Corpus.objects.get_or_create(name=corpus_name)[0]
        for fil in files:
            #try:
                #print(fil)
                #import ipdb; ipdb.set_trace()
            f = fil.read().decode()
            author = Author.objects.get_or_create(name=find_author(f))[0]
            Text.objects.create(title = find_title(f), text = find_text(f), corpus = corpus, author = author, year = find_year(f))
            #except: 
            #    print("failed")
            #    pass
                
    
    def parse_folder(self, foldername, corpus_name):
        corpus = Corpus.objects.get_or_create(name=corpus_name)[0]
        for filename in os.listdir(foldername):
            try:
                path = '/'.join([foldername, filename])
                f = open( path, 'r', encoding='utf-8').read()
                print(filename)
                author = Author.objects.get_or_create(name=find_author(f))[0]
                Text.objects.create(title = find_title(f), text = find_text(f), corpus = corpus, author = author, year = find_year(f))
            except:
                print("failed")
                pass

def fill_text_data(text_obj):
    print('will_text_data started')
    print('making wordlist')
    wordlist = make_wordlist(text_obj.text)
    print('counting occurrences')
    counted_words = make_count_wordlist(wordlist)
    # make words in wordlist unique
    wordlist = list(set(wordlist))
    print('finding existing word objects')
    existing = set(Word.objects.all().values_list('word', flat=True))
    print('%s existing words found' % len(existing))
    print('clearing wordlist')
    wordlist = list(filter(lambda w: w not in existing, wordlist))
    # now wordlist only contains words not known in db
    print('making %s new word objects' % len(wordlist))
    new_words = list(map(create_word_object, wordlist))
    print('bulk saving %s new words to db' % len(new_words))
    Word.objects.bulk_create(new_words)
    print('making %s word in text count objects' % len(counted_words))
    words_dict = { w: i for w, i in Word.objects.all().values_list('word', 'id') }
    word_in_text_counts = [create_word_in_text_count_object(words_dict[w], v, text_obj) for w, v in counted_words.items()]
    print('bulk saving %s word in text count objects' % len(word_in_text_counts))
    WordInTextCount.objects.bulk_create(word_in_text_counts)
    print('fill_text_data finished')

def create_word_object(word_str):
    return Word(word = word_str, stemmed = stem_word_porter2(word_str))

def create_word_in_text_count_object(word, count, text):
    return WordInTextCount(word_id= word, text = text, count = count)
    
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
        author = result.groups()[1]
        author = author.replace('[', '')
        author = author.replace(']', '')
        return author

def find_title(content):
    title = find_tag_content('title', content) 
    if not title:
        title = 'UNKNOWN'
    return title

def find_year(content):
    year = find_tag_content('year', content)
    year = re.search(r'[0-9]{4}', year)
    if not year:
        year = '0';
    return year.group()

def find_tag_content(tag, xmltext):
    pattern = re.compile('(<{0}>)([^<]*)(</{0}>)'.format(tag), re.IGNORECASE)
    return pattern.search(xmltext).groups()[1]

def find_text(content):
    pattern = re.compile('(<text>)(.*)(</text>)', re.IGNORECASE | re.DOTALL)
    return pattern.search(content).groups()[1]
