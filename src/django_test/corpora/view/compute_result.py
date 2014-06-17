from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount

from django.http import HttpResponse
# Create your views here.


def textfinder(request):
    text = Text.objects.all()
    
    if(request.POST.get("y_from")!=""):
        text = text.filter(year__gte=request.POST.get("y_from"))
 
    if(request.POST.get("y_to")!=""):
        text = text.filter(year__lte=request.POST.get("y_to"))

    if(request.POST.getlist("authors")):
        authors=Author.objects.all().filter(name__in=request.POST.getlist("authors")).values_list('id', flat=True)
        text = text.filter(author__in=authors)

    if(request.POST.get("in_title")!=""):
        text=text.filter(title_contains=request.POST.get("in_title"))

    return text

    


def compute_result(request):
    
    texts = textfinder(request)
    return render(request, 'compute/compute_result.html', 
            {
            'text_list': texts
            }
            )


