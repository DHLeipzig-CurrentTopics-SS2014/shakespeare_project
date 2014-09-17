from calculations import util
from corpora.models import *
import re

class BookWithMostWords:
    def url(self):
        return "books_with_most_words"
    
    def name(self):
        # shown in the navigation
        return "Books with Most Words"
    
    def title(self):
        # title for the page
        return "What could this mean?"
    
    def calc(self, parsed_request):
        
        texts = util.get_texts_from_authors_in_timespan(parsed_request['authors'], parsed_request['timespan'])
        words = parsed_request['words']
    
        wctxts={}

        for text in texts:
            wtcs = WordInTextCount.objects.filter(text=text)
            count=0
            for word in words:
                counts = wtcs.filter(word__word=word)
                if len(counts) > 0:
                    count += counts.first().count
            wctxts[text.title]=count
        
        wctxts=sorted(wctxts.items(), key=lambda x: x[1])
        
        xs=[author for author, ratio in wctxts]
        ys =[ratio for author, ratio in wctxts]

        return {'x': xs, 'y': ys}
