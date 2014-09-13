# NOT TESTED
# COULD BE FASTER WITH MAP REDUCE

from corpora.calulations import compute_result # don't know if this works

def shakeWordsYear(request):
    texts = textfinder(request)
    spw = SearchWord.objects.all()
    r = re.compile('[.,:;_]')
    words = list(map(str.strip, r.split(request.POST.get('words'))))
    y_from = texts.earliest('year').year
    y_to = texts.latest('year').year
    wcounts = {}
    for text in texts:
        for word in words:
            if (word in spw):
                if not text.year in wcounts:
                    wcounts[text.year] = {}
                if not word in wcounts[text.year]:
                    wcounts[text.year][word] = 0
                wcounts[text.year][word] += 1
    
    result = {}
    for year in wcounts:
        maxWord = (0,"None")
        for word in wcounts[year]:
            if wcounts[year][word] > maxWord[0]:
                maxWord = (wcounts[year][word],word)
        result[year] = maxWord[1]
    

    return {
            'result': result
           }
