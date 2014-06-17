from django.shortcuts import render, get_object_or_404
from corpora.models import Author, Text, Word, WordInTextCount

from django.http import HttpResponse
# Create your views here.

def compute_erg(request):
    j_von=request.POST.get("j_von","")
    j_bis=request.POST.get("j_bis","")

    return render(request, 'compute/compute_erg.html', 
            {"j_von" : j_von,
            "j_bis" : j_bis}
            )
