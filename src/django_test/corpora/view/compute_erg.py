from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount

from django.http import HttpResponse
# Create your views here.

def compute_erg(request):
    y_from=request.POST.get("y_from","")
    y_to=request.POST.get("y_to","")

    return render(request, 'compute/compute_erg.html', 
            {"y_from" : y_from,
            "y_to" : y_to}
            )


