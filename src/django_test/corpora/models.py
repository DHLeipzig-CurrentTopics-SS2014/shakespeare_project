from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    birthyear = models.IntegerField(null=True)
    deathyear = models.IntegerField(null=True)
    places = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Text(models.Model):
    author = models.ForeignKey(Author)
    text = models.TextField()
    title = models.CharField(max_length=40)
    year = models.IntegerField(null=True)

    def __str__(self):
        return self.title

    def word_list(self):
        # returns a list of words of the text, everything which is not a letter will be removed!
        return clean_from_nonletters(self.text).split()

    def clean_from_nonletters(text):
        return re.sub(r'[^a-zA-Z\s]', ' ', text)