#!/usr/env/python3

from stemming_lib.stemming.porter2 import stem as porter2
from stemming_lib.stemming.lovins import stem as lovins
from stemming_lib.stemming.paicehusk import stem as paicehusk

from lxml import etree

def stem_word_porter2(word):
    return porter2(word)

def stem_word_lovins(word):
    return lovins(word)

def stem_word_paicehusk(word):
    return paicehusk(word)

xml = etree.parse("./test.xml",parser=etree.HTMLParser())


for word in xml.xpath("//w"):
    w=(etree.tostring(word,encoding="unicode",method="text")).strip()
    word.set("stemmed_porter2",stem_word_porter2(w))
    word.set("stemmed_lovins",stem_word_lovins(w))
    word.set("stemmed_paicehusk",stem_word_paicehusk(w))

xml.write("output.xml")
