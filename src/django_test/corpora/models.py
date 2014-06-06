from django.db import models

class SearchWord(models.Model):
    word = models.CharField(max_length=30)
    stemmed = models.CharField(max_length=30)

class Corpus(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    places = models.CharField(max_length=200)
    birthyear = models.IntegerField(null=True)
    deathyear = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Text(models.Model):
    corpus = models.ForeignKey(Corpus)
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=40)
    text = models.TextField()
    year = models.IntegerField(null=True)

    def __str__(self):
        return self.title 

    
class Word(models.Model):
    word = models.CharField(max_length=30)
    stemmed = models.CharField(max_length=30)
    in_text_count = models.ManyToManyField(Text, through='WordInTextCount')

    def __str__(self):
        return ' - '.join([self.word, self. stemmed])

class WordInTextCount(models.Model):
    word = models.ForeignKey(Word)
    text = models.ForeignKey(Text)
    count = models.IntegerField(null=False)
