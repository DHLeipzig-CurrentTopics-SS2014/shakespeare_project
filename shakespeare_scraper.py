#!/usr/bin/python3
import re
from lxml import etree

base_url = "http://shakespeare.mit.edu/"
texts = ["allswell", "asyoulikeit", "comedy_errors", "cymbeline", "lll", "measure", "merry_wives", "merchant", "midsummer", "much_ado", "pericles", "taming_shrew", "tempest", "troilus_cressida", "twelfth_night", "two_gentlemen", "winters_tale", "1henryiv", "2henryiv", "henryv", "1henryvi", "2henryvi", "3henryvi", "henryviii", "john", "richardii", "richardiii", "cleopatra", "coriolanus", "hamlet", "julius_caesar", "lear", "macbeth", "othello", "romeo_juliet", "timon", "titus"]
full = "/full.html"

def parse_book(book):
    xmlpage = etree.parse(''.join([base_url,book,full]), parser = etree.HTMLParser())
    text = ""
    # looking for text within A block with attribute NAME following an enumeration scheme (starts with number seems to be a sufficient test)     
    for a in xmlpage.xpath('.//a'):
        if a.get('name') and re.match(r'[0-9]', a.get('name')):
            line = a.text.strip()
            text += line
            text += "\n"
    return text


for text in texts:
    f = open(''.join(['texts/', text, '.txt']), 'wt', encoding='utf-8')
    f.write(parse_book(text))
    f.close()

'''
Matt's notes:
Nicely done.  It downloads the texts very nicely.
Full credit.
'''
