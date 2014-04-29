#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import os, re

URL='http://www.oed.com/search?browseType=sortAlpha&case-insensitive=true&ch_firstSource=William+Shakespeare&nearDistance=1&ordered=false&page={}&pageSize=100&scope=ENTRY&sort=entry&type=dictionarysearch'

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
        f.write(word+", "+url+"\n")
f.close()