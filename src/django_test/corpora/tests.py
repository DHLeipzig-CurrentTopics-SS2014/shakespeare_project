from django.test import TestCase
from corpora.tools import corpus_parser
from corpora.models import Author, Text, Corpus, Word, WordInTextCount

class CorpusParserTestCase(TestCase):
    def setUp(self):
        self.corpus = Corpus.objects.create(name="corpus")
        self.author = Author.objects.create(name="author")
        self.text="hello world hello world python"
        self.text_object = Text.objects.create(title="title", text=self.text, author=self.author, corpus=self.corpus)

    def test_wordlist_creates_list_of_words(self):
        wordlist = corpus_parser.make_wordlist(self.text)
        self.assertEqual(wordlist, ["hello", "world", "hello", "world", "python"])
    def test_make_count_wordlist_works(self):
        wordlist = corpus_parser.make_count_wordlist(corpus_parser.make_wordlist(self.text))
        self.assertEqual(wordlist, {'hello': 2, 'world': 2, 'python': 1})

    def test_create_wordintextcount_object_should_work(self):
        w = Word.objects.create(word="hello", stemmed="hell")
        witc = corpus_parser.create_word_in_text_count_object("hello", 3, self.text_object)
        self.assertIsNotNone(witc)
        self.assertEqual(witc.count, 3)
        self.assertEqual(witc.word, w)
        witc.save()

    def test_wordintextcount_should_keep_values(self):
        w = Word.objects.create(word="hello", stemmed="hell")
        witc = corpus_parser.create_word_in_text_count_object("hello", 3, self.text_object)
        witc.save()
        witc_obj = WordInTextCount.objects.get(word=w, text=self.text_object)
        self.assertEqual(witc_obj.count, 3)

    def test_build_text_should_create_text_and_word_and_wordintextcount_entries(self):
        corpus_parser.build_text("title", self.text, self.corpus, self.author, 1234)
        w = Word.objects.filter(word='hello')
        self.assertNotEqual(w, [])
        list(map(lambda x: print(x.count),WordInTextCount.objects.all() ))
        
        witc_obj = WordInTextCount.objects.get(word=w[0], text=self.text_object)
        self.assertEqual(witc_obj.count, 2)
        




