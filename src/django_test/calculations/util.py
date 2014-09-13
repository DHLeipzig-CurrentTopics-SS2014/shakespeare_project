from corpora.models import *
import re
import pandas as pd

def get_texts_from_authors_in_timespan(authors, timespan):
    texts = Text.objects.filter(author__name__in = authors)
    if(timespan[0] != -1):
        texts = texts.filter(year__gte = str(timespan[0]))
    if(timespan[1] != -1):
        texts = texts.filter(year__lte = str(timespan[1]))
    return texts

def filter_authors(author_str_list):
    # if objects in the list authors are filtered by the given names, otherwise all authors are returned.
    if(len(authors) > 0):
        authors=Author.objects.all().filter(name__in=author_str_list).values_list('id', flat=True)
    else:
        authors = Author.objects.all()
    return authors


def group_texts_by_interval(texts, y_interval):
    # a hash with pairs of ints (interval_begin, interval_end) as keys, list of the text objects as values
    texts = texts.order_by('year')
    Y_INTERVAL = y_interval
    y_from = texts.earliest('year').year
    y_to = texts.latest('year').year
    text_year_dict = {}
    y_current = y_from + Y_INTERVAL
    while (y_current  <= y_to + Y_INTERVAL):
       text_year_dict[(y_current - Y_INTERVAL, y_current)] = texts.filter(year__gte = y_current - Y_INTERVAL).filter(year__lt = y_current)
       y_current += Y_INTERVAL
    return text_year_dict

def texts_to_data_frames(texts_dict, stem):
    y_df_dict = {}
    for y_interval, texts in texts_dict.items():
       y_texts_dict = {}
       for text in texts:
           word_counts = WordInTextCount.objects.filter(text = text).values_list('word__%s' % 'stemmed' if stem else 'word', 'count')
           y_texts_dict[text.title] = { x[0]:x[1] for x in word_counts }
       text_df = pd.DataFrame(y_texts_dict).fillna(0)
       y_df_dict[y_interval] = text_df
    return y_df_dict
