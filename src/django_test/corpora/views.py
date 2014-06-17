from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount

from django.http import HttpResponse
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
    authors = Author.objects.all().order_by('name')
    return render(request, 'compute/index.html',{'author_list': authors})

def compute_erg(request):
    y_from=request.POST.get("y_from","")
    y_to=request.POST.get("y_to","")







