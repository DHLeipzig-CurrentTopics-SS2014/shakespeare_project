from django.shortcuts import render
from calculations.questions.example_question import ExampleQuestion
from calculations.questions.booksMostShakeWords import BookWithMostWords
from calculations.questions.words_per_year import WordsPerYear
from calculations import form_parser
from corpora.models import *
from os import listdir
from os.path import isfile,join,exists

calculations_available = [ExampleQuestion, BookWithMostWords, WordsPerYear]
# each calculation available must be set up in this list and provide a function below. mind that you need to put an url in this apps urls.py!

def index(request):
    authors = Author.objects.all().order_by('name')    
    #next Get all Files: vom Textcollection ordner    
    path="corpora/textcollections/"
    files = [f for f in listdir(path) if isfile(join(path,f))]

    return render(request, 'index.html', {'questions': calculations_available, 'author_list': authors,'textcoll':files})

