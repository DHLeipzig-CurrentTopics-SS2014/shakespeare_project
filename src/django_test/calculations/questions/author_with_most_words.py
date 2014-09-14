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
        # your calculations
        words = parsed_request['words']
        authors = util.filter_authors(parsed_request['authors'])
        authors_texts = { author: author.text_set.all() for author in authors }
        authors_wtcs = { author: [ text.wordintextcount_set.all() for text in texts ] for author, texts in authors_texts.items() }
        authors_wtcs_filtered = { author: list(filter(lambda x: x in words, [ wtc for wtc in wtcs])) for author, wtcs in authors_wtcs.items()}
        
        
        xs=[]
        ys =[]    
      # TODO das funktioniert oben noch nicht
      # wtcs zählen
      # sortieren -> die höchstgerankten autoren ausgeben

    
        xs = '[' + ','.join(map(str, xs)) + ']'
        ys = '[' + ','.join(map(str, ys)) + ']'
        return {
                'text_list': "",
                'x': xs,
                'y': ys
                }
