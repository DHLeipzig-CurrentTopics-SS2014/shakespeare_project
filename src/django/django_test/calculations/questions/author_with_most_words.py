from calculations import util
from corpora.models import *
import re

class AuthorWithMostWords:
    def url(self):
        return "author_with_most_words"
    
    def title(self):
        # title for the page
        return "Authors that used the words at most"
    
    def name(self):
        # shown in the navigation
        return "Words/Author"
    
    def calc(self, parsed_request):        
        words = parsed_request['words']
        authors = util.filter_authors(parsed_request['authors'])
        authors_texts={}

        for author in authors:
            authors_texts[author.name]=util.get_texts_from_authors_in_timespan([author.name], parsed_request['timespan'])
        
        authors_wtcs = { author: flatten_list([ text.wordintextcount_set.values_list('word__word', 'count') for text in texts ]) for author, texts in authors_texts.items() }
        authors_wtcs_filtered = { author: list(filter(lambda x: x[0] in words, tcs)) for author, tcs in authors_wtcs.items() }
    
        authors_wtcs_totals = { author: sum(map(lambda t: t[1], tcs)) for author, tcs in authors_wtcs.items() }
        authors_wtcs_filtered_totals = { author: sum(map(lambda t: t[1], tcs)) for author, tcs in authors_wtcs_filtered.items() }
        
        authors_word_ratio = []
        for author, count in authors_wtcs_totals.items():
            authors_word_ratio.append((author, authors_wtcs_filtered_totals[author]))
        authors_word_ratio = sorted(authors_word_ratio, key=lambda c: c[1])

        xs=[author for author, ratio in authors_word_ratio]
        ys =[ratio for author, ratio in authors_word_ratio]

        return {
                'text_list': "",
                'x': xs,
                'y': ys
                }

def find_wordintextcounts(wtcs, words):
    res = list(map(lambda w: count_or_none(wtcs, w), words))
    return filter(lambda c: c != None, res)

def count_or_none(wtcs, w):
    wtc = wtcs.filter(word__word=w).first()
    if(wtc):
        return wtc.count
    else:
        return None
    
def flatten_list(l):
    return [item for sublist in l for item in sublist]
