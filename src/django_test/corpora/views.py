import pandas as pd
from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount
import math
from sklearn.feature_extraction.text import TfidfTransformer
from django.http import HttpResponse
import numpy as np

# Folderview import by @Thomas Döring
from os import listdir
from os.path import isfile,join,exists

# Create your views here.

def author_index(request):
    authors = Author.objects.all().order_by('name')
    return render(request, 'authors/index.html', {'author_list': authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    texts = Text.objects.filter(author_id=author_id)
    return render(request, 'authors/detail.html', {'author': author, 'texts':texts})

def text_index(request):
    authors = Text.objects.all().order_by('title')
    return render(request, 'texts/index.html', {'text_list': authors})

def text_detail(request, text_id):
    return render(request, 'texts/detail.html', {'text': get_object_or_404(Text, pk=text_id)})

def text_words(request, text_id):
    words = WordInTextCount.objects.filter(text__id=text_id)
    return render(request, 'texts/words.html', {'word_text_counts': words})

def compute_index(request):
    # Authors
    authors = Author.objects.all().order_by('name')
    
    #next Get all Files: vom Textcollection ordner
    
    path="corpora/textcollections/"
    files = [f for f in listdir(path) if isfile(join(path,f))]

    return render(request, 'compute/index.html',{'author_list': authors,'textcoll':files})

# auxilary function for compute_result
def textfinder(request):
    Y_INTERVAL = 5
    texts = Text.objects.all().order_by('year')

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

    text_year_dict = {}
    y_current = y_from + Y_INTERVAL
    while (y_current  <= y_to + Y_INTERVAL):
       text_year_dict[(y_current - Y_INTERVAL, y_current)] = texts.filter(year__gte = y_current - Y_INTERVAL).filter(year__lt = y_current)
       y_current += Y_INTERVAL

    return text_year_dict

def getTfidfDFs(texts_dict):
    y_df_dict = {}
    for y_interval, texts in texts_dict.items():
       y_texts_dict = {} 
       for text in texts:
           word_counts = WordInTextCount.objects.filter(text = text)
           y_texts_dict[text.title] = {w.word.word : w.count for w in word_counts}
           text_df = pd.DataFrame(y_texts_dict).fillna(0)
           tfidf = TfidfTransformer().fit_transform(text_df)
           tfidf_matrix = pd.DataFrame(data = tfidf.toarray(), index =text_df.index, columns = text_df.columns)
           y_df_dict[y_interval] = tfidf_matrix
    return y_df_dict

def compute_result(request):
    texts_dict = textfinder(request)
    tfidf_dfs = getTfidfDFs(texts_dict)

    return render(request, 'compute/compute_result.html', 
            {
            'text_list': "",
            'x': "[ 1, 2, 3 ]",
            'y': "[ 4, 2, 5 ]"
            }
            )
