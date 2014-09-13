from calculations import util
from corpora.models import *
import re

class WordsPerYear:
    def url(self):
        return "words_per_year"
    
    def title(self):
        # title for the page
        return "Shows"
    
    def name(self):
        # shown in the navigation
        return "Words/Year"
    
    def calc(self, parsed_request):
        # your calculations
        texts = util.get_texts_from_authors_in_timespan(parsed_request['authors'], parsed_request['timespan'])
        r = re.compile('[.,:;_]')
        words = parsed_request['words']
        y_from = texts.earliest('year').year
        y_to = texts.latest('year').year
        # word -> list, entry for each year
        wcounts = { w: ([0] * (y_to - y_from + 1)) for w in words }
        for text in texts:
            wtcs = WordInTextCount.objects.filter(text=text)
            for word in words:
                counts = wtcs.filter(word__word=word)
                if len(counts) > 0:
                    wcounts[word][text.year - y_from] += counts.first().count
    
        xs = list(range(y_from, y_to + 1))
        ys = [0] * (y_to - y_from + 1)
        for w in wcounts:
            ys = [x + y for x, y in zip(wcounts[w], ys)]
    
        xs = '[' + ','.join(map(str, xs)) + ']'
        ys = '[' + ','.join(map(str, ys)) + ']'
        return {
                'text_list': "",
                'x': xs,
                'y': ys
                }
