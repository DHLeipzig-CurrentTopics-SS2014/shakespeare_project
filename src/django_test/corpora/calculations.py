from corpora.models import Author, Text, Word, WordInTextCount, Corpus
import math
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd
import re

# auxilary function for compute_result
def textfinder(request):
    texts = Text.objects.all()

    if(request.POST.getlist("authors")):
        authors=Author.objects.all().filter(name__in=request.POST.getlist("authors")).values_list('id', flat=True)
        texts = texts.filter(author__in=authors)

    if(request.POST.get("in_title")!=""):
        texts=texts.filter(title_contains=request.POST.get("in_title"))

    y_from = request.POST.get("y_from")
    y_from = texts[0].year if y_from == "" else int(y_from)
    texts = texts.filter(year__gte = str(y_from))
    
    y_to = request.POST.get("y_to")
    y_to = texts.last().year if y_to == "" else int(y_to) 
    texts = texts.filter(year__lte=str(y_to))
    return texts
    
def group_by_interval(texts, y_interval):
    texts = texts.order_by('year')
    Y_INTERVAL = y_interval
    y_from = texts.earliest('year').year
    y_to = texts.latest('year').year
    text_year_dict = {}
    y_current = y_from + Y_INTERVAL
    while (y_current  <= y_to + Y_INTERVAL):
       text_year_dict[(y_current - Y_INTERVAL, y_current)] = texts.filter(year__gte = y_current - Y_INTERVAL).filter(year__lt = y_current)
       y_current += Y_INTERVAL

    return text_year_dict

def textsToDataFrames(texts_dict, stem):
    y_df_dict = {}
    for y_interval, texts in texts_dict.items():
       y_texts_dict = {} 
       for text in texts:
           word_counts = WordInTextCount.objects.filter(text = text).values_list('word__%s' % 'stemmed' if stem else 'word', 'count')
           y_texts_dict[text.title] = { x[0]:x[1] for x in word_counts }
       text_df = pd.DataFrame(y_texts_dict).fillna(0)
       y_df_dict[y_interval] = text_df
    return y_df_dict

def tfidf(texts_df):
    result = {}
    for y_interval, text_df in texts_df.items():
        result[y_interval] = pd.DataFrame(data = TfidfTransformer().fit_transform(text_df).toarray(), index =text_df.index, columns = text_df.columns)
    return result

def id_function(texts_df):
   return texts_df
   
def compute_result(request):

    # dict with possible calculations
    calc_options = {'tfidf':tfidf,
                    'id':id_function}

    texts_dict = group_by_interval(textfinder(request), 5)
    text_dfs = textsToDataFrames(texts_dict, True if request.POST.get('stem') == 'on' else False)
    
    result = calc_options[request.POST.get('function')](text_dfs)
    
    if (request.POST.get('uploadtype') == 'uploaded_file'):
        words = request.FILES['upload_file'].read().decode("utf-8").split('\n')
    else:
        words = open('corpora/textcollections/' + request.POST.get('wordlist'), 'r').read().split('\n')
    
    for y_interval in result.keys():
        word_df = pd.DataFrame(index = words, columns = result[y_interval].keys()).fillna(0)
        result[y_interval] = pd.merge(result[y_interval], word_df, left_index=True, right_index=True)
        result[y_interval] = result[y_interval].mean().mean(axis = 1)

    x = []
    y = []    
    for period in sorted(result.keys()):
        x.append(str(period[0]+(period[1]-period[0])/2))
        if not np.isnan(result[period]): 
            y.append(str(result[period]))
        else:
            print("ERROR: NAN VALUES")
            y.append("0")

    x = '[' + ','.join(x) + ']'
    y = '[' + ','.join(y) + ']'
        
    return {
            'text_list': "",
            'x': x,
            'y': y
            }


def words_per_year(request):
    texts = textfinder(request)
    r = re.compile('[.,:;_]')
    words = r.split(request.POST.get('words')).strip()    
    y_from = texts.earliest('year').year
    y_to = texts.latest('year').year
    wcounts = {w: ([0]*(y_to-y_from)) for w in words}
    
    
    
    
    #return result
    