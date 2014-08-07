from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount, Corpus
from django.http import HttpResponse
from corpora.tools.corpus_parser import CorpusParser
import corpora.calculations as calc

# Folderview import by @Thomas Döring
from os import listdir
from os.path import isfile,join,exists

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
    authors = Author.objects.all().order_by('name')    
    #next Get all Files: vom Textcollection ordner    
    path="corpora/textcollections/"
    files = [f for f in listdir(path) if isfile(join(path,f))]
    return render(request, 'compute/index.html',{'author_list': authors,'textcoll':files})

def compute_result(request):
    return render(request, 'compute/compute_result.html', calc.compute_result(request))

def corpora_index(request):
    corpora = Corpus.objects.all()
    return render(request, 'corpora/index.html', {'corpora': corpora})

def corpora_upload(request):
    cp = CorpusParser()
    cp.parse_files(request.FILES.getlist('corpus_files'), request.POST.get("corpus_name"))
    return render(request, 'corpora/upload.html')
