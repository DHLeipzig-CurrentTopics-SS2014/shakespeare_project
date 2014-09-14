from django.conf.urls import patterns, url
from calculations import views


urlpatterns = patterns('', 
    # /calculations/
    url(r'^$', views.index, name='index'),
    url(r'choose_calc/$', views.choose_calc, name='choose_calc'),
    url(r'words_per_year/$', views.words_per_year, name='words_per_year'),
    url(r'example/$', views.example_question, name='example'),
    url(r'tfidf/$', views.tfidf, name='tfidf'),
    url(r'books_with_most_words/$', views.books_with_most_words, name='books_with_most_words'),
    url(r'author_with_most_words/$', views.author_with_most_words, name='author_with_most_words'),
    
        
    )