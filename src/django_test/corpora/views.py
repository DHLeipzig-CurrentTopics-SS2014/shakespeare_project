import pandas as pd
from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount, Corpus
import math
from sklearn.feature_extraction.text import TfidfTransformer
from django.http import HttpResponse
import numpy as np
from corpora.tools.corpus_parser import CorpusParser

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

def textsToDataFrames(texts_dict):
    y_df_dict = {}
    for y_interval, texts in texts_dict.items():
       y_texts_dict = {} 
       for text in texts:
           word_counts = WordInTextCount.objects.filter(text = text)
           y_texts_dict[text.title] = {w.word.word : w.count for w in word_counts}
           text_df = pd.DataFrame(y_texts_dict).fillna(0)
           
           y_df_dict[y_interval] = text_df
    return y_df_dict

def tfidf(texts_df):
    result = {}
    for y_interval, text_df in texts_df.items():
        result[y_interval] = pd.DataFrame(data = TfidfTransformer().fit_transform(text_df).toarray(), index =text_df.index, columns = text_df.columns)
    return result

def compute_result(request):

    # dict with possible calculations
    calc_options = {'tfidf':tfidf}

    texts_dict = textfinder(request)
    text_dfs = textsToDataFrames(texts_dict)
    
    result = calc_options[request.POST.get('function')](text_dfs)
    
    if (request.POST.get('uploadtype') == 'uploaded_file'):
        words = request.FILES['upload_file'].read().decode("utf-8").split('\n')
    else:
        words = open('corpora/textcollections/' + request.POST.get('wordlist'), 'r').read().split('\n')
    
    #word_df = pd.DataFrame(index = words, columns = result.keys())
    #äprint(word_df)
    #print(result)
    
    for y_interval in result.keys():
        word_df = pd.DataFrame(index = words, columns = result[y_interval].keys()).fillna(0)
        #result[y_interval] = (result[y_interval] + word_df)[words].fillna(0)
        result[y_interval] = pd.merge(result[y_interval], word_df, left_index=True, right_index=True)
        result[y_interval] = result[y_interval].mean().sum(axis = 1)

    x = []
    y = []    
    for period in sorted(result.keys()):
        #x.append(str((period[1]-period[0])/2))
        x.append(str(period[0]+(period[1]-period[0])/2))
        y.append(str(result[period]))


    x = '[' + ','.join(x) + ']'
    y = '[' + ','.join(y) + ']'
        
    return render(request, 'compute/compute_result.html', 
            {
            'text_list': "",
            'x': x,
            'y': y
            }
            )


def get_count_of_stem(stem):
    WordInTextCount.objects.filter(word__stemmed = stem)
    # TODO weitermachen...



def corpora_index(request):
    corpora = Corpus.objects.all()
    return render(request, 'corpora/index.html', {'corpora': corpora})

def corpora_upload(request):
    cp = CorpusParser()
    cp.parse_files(request.FILES, request.POST.get("corpus_name"))
    return render(request, 'corpora/index.html')
