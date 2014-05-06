#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from itertools import chain
import os, re

URL='http://www.oed.com/search?browseType=sortAlpha&case-insensitive=true&ch_firstSource=William+Shakespeare&nearDistance=1&ordered=false&page={}&pageSize=100&scope=ENTRY&sort=entry&type=dictionarysearch'

# from http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
def stringify_children(node):
    parts = ([node.text] +
            list(chain(*([c.text, etree.tostring(c).decode("utf-8"), c.tail] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

# delete old version
if os.path.isfile("output.csv"):
    os.remove('output.csv')

# open output file
f = open('output.csv','at', encoding='utf-8')

# crawl recursively forever because of a typo in LAST_PAGE
for page in range(1,17):
    print("crawling page {} of 16".format(page))
    xml = etree.parse(URL.format(page), parser = etree.HTMLParser())
    for result in xml.xpath(".//span[@class = 'word']"):
        url = "http://www.oed.com" + result.xpath(".//a[@title = 'see this full entry']")[0].get("href")
        word = result.xpath(".//span[@class = 'hw']")[0].text
        word = re.sub(r"[ˈˌ]+",'',word) # evtl. \- mit rein?
        print("  {}".format(word));
        detail = etree.parse(url, parser = etree.HTMLParser())
        quoteslist = []
        write = word+", "+url + "[";
        quoteroot = detail.getroot()
        if quoteroot is not None:
            for quotes in quoteroot.xpath(".//div[@class = 'quotationsBlock']"):
                write += stringify_children(quotes)+", "
        else:
            write += "ERROR"
        write += "]"
        f.write(write+"\n")
f.close()