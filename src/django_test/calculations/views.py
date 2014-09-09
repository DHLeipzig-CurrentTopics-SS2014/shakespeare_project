from django.shortcuts import render
from calculations.questions.example_question import ExampleQuestion
from calculations.questions.booksMostShakeWords import BookWithMostWords

calculations_available = [ExampleQuestion, BookWithMostWords]
# each calculation available must be set up in this list and provide a function below. mind that you need to put an url in this apps urls.py!

def index(request):
    return render(request, 'index.html', {'questions': calculations_available})