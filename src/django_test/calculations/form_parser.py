
def parse_data_input_form(request):
    # return a hash of interpreted data from the form. The hash has the following fields:
    # 'timespan': a pair of ints, first y_from, second y_to. if a year was not stated by the user value is -1
    # 'authors': list of chosen authors names (str). empty if none were chosen
    # 'words': the words that were chosen by the user. if a file was uploaded this will be taken first,
    # if words were given in the form field these are taken, otherwise the wordlist stated. 
    return { 'timespan': parse_timespan(request),
            'authors': parse_authors(request),
            'words': parse_words_decision(request)}
    
def parse_words_decision(request):
    if (request.FILES['upload_file']):
        words = request.FILES['upload_file'].read().decode("utf-8").split('\n')
    elif(request.POST.get('words') != ''):
        r = re.compile('[.,:;_]')
        words = list(map(str.strip, r.split(request.POST.get('words'))))
    else:
        words = open('corpora/textcollections/' + request.POST.get('wordlist'), 'r').read().split('\n')
    return words
    
def parse_authors(request):
    return request.POST.getlist("authors")

def parse_timespan(request):
    y_from = request.POST.get("y_from")
    y_from = -1 if y_from == "" else int(y_from)

    y_to = request.POST.get("y_to")
    y_to = -1 if y_to == "" else int(y_to)
    
    return (y_from, y_to)