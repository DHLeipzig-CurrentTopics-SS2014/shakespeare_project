from django.shortcuts import render
from calculations.questions.booksMostShakeWords import BookWithMostWords
from calculations.questions.author_with_most_words import AuthorWithMostWords
from calculations.questions.words_per_year import WordsPerYear
from calculations.questions.tfidf import TFIDF
from calculations import form_parser
from corpora.models import *
from os import listdir
from os.path import isfile,join,exists

calculations_available = [BookWithMostWords, WordsPerYear, TFIDF, AuthorWithMostWords]
# each calculation available must be set up in this list and provide a function below. mind that you need to put an url in this apps urls.py!

def index(request):
    authors = Author.objects.all().order_by('name')    
    #next Get all Files: vom Textcollection ordner    
    path="corpora/textcollections/"
    files = [f for f in listdir(path) if isfile(join(path,f))]

    options = { 'author_list': authors,'textcoll':files }
    if("input_data" in request.session):
        options['questions'] = calculations_available
    return render(request, 'index.html', options)

def choose_calc(request):
    input_data = form_parser.parse_data_input_form(request)
    store_input_for_session(request.session, input_data)
    return render(request, 'choose_calc.html', {'questions': calculations_available} )
    
    
def store_input_for_session(session, input_data):
    session['input_data'] = input_data

def words_per_year(request):
    return process_graph_constructing_question(request, WordsPerYear,'graph')

def books_with_most_words(request):
    return process_graph_constructing_question(request, BookWithMostWords)

def author_with_most_words(request):
    return process_graph_constructing_question(request, AuthorWithMostWords)

def tfidf(request):
    return process_graph_constructing_question(request, TFIDF,'graph')

def process_graph_constructing_question(request, question_class, visualization='text'):
    if(not request.session['input_data']):
        return redirect('/calculations/')
    calc = question_class()
    result = calc.calc(request.session['input_data'])
    if(visualization == 'graph'):
        return make_graph(request, calc, result)
    elif(visualization == 'bar'):
        return make_bars(request, calc, result)
    else:
        return make_text(request, calc, result)
    
def make_graph(request, calc, result):
    return render(request, 'result_graph.html', {'x': result['x'], 'y': result['y'], 'questions': calculations_available, 'active': calc.url()})

def make_bars(request, calc, result):
    return render(request, 'result_bar_chart.html', {'x': result['x'], 'y': result['y'], 'questions': calculations_available, 'active': calc.url()})

def make_text(request, calc, result):
    list = zip(result['x'],result['y'])
    return render(request, 'result_text.html', {'list':list, 'questions': calculations_available, 'active': calc.url()})

