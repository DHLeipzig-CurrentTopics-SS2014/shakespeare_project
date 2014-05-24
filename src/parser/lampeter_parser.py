#!/usr/bin/python3

import re
import os
from lxml import etree

def find_title(content):
    pattern = re.compile('(<TITLE>)([^<]*)(</TITLE>)', re.IGNORECASE)
    return pattern.search(content).groups()[1]

def find_author(content):
    pattern = re.compile('(<PERSNAME>)([^<]*)(</PERSNAME>)', re.IGNORECASE)
    result = pattern.search(content)
    if result == None:
        return 'unknown'
    else:
       return result.groups()[1]

def find_date(content):
    pattern = re.compile('(<DATE>)([^<]*)(</DATE>)', re.IGNORECASE)
    date_content = pattern.search(content).groups()[1]
    if len(date_content) == 4:
        return date_content
    else:
        pattern = re.compile('[0-9]{4,4}')
        return pattern.search(date_content).group()

def find_text(content):
    pattern = re.compile('(<body>)(.*)(</body>)', re.IGNORECASE | re.DOTALL)
    return pattern.search(content).groups()[1]

def clean_from_nonletters(text):
    return re.sub(r'[^a-zA-Z\s]', ' ', text)

def clean_from_markup(text):
    pattern = re.compile('<.*?>', re.IGNORECASE | re.DOTALL)
    return pattern.sub('', text)

def clean_from_entities(text):
    pattern = re.compile('&[a-zA-Z]{1,10};', re.IGNORECASE)
    return pattern.sub('', text)

def parse_document(filename):
    doc = open(filename, 'r', encoding='iso-8859-15').read()
    result = {}
    result['title'] = find_title(doc)
    result['author'] = find_author(doc)
    result['date'] = find_date(doc)
    result['textlist'] = clean_from_nonletters(clean_from_markup(clean_from_entities(find_text(doc)))).split()
    return result

def build_xml(doc_dict):
    xml = etree.Element('xml')
    author = etree.SubElement(xml, 'author')
    author.text = doc_dict['author']
    year = etree.SubElement(xml, 'year')
    year.text = doc_dict['date']
    title = etree.SubElement(xml, 'title')
    title.text = doc_dict['title']
    text = etree.SubElement(xml, 'text')
    for index, word in enumerate(doc_dict['textlist']):
        w = etree.SubElement(text, 'w', id=str(index))
        w.text = word
    return xml



for filename in os.listdir('Input/'):
    xml = build_xml(parse_document(''.join(['Input/', filename])))
    out = open(''.join(['Output/', filename.replace('txt', 'xml')]), 'w', encoding='utf-8')
    out.write(etree.tostring(xml, pretty_print=True, encoding=str))
    print(filename, ' finished')

