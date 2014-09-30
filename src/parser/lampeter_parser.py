#!/usr/bin/env python3
####################################
#
# usage: ./lampeter_parser.py <Lampeter_txt.zip> <output_dir>
#
# SHA256 (Lampeter_txt.zip) = 2c6f644290e7cd1fac10c284fe149f16594ca047342bc34e077099f4ede74e01
# MD5 (Lampeter_txt.zip) = e7ad33f4b2ab16a7affd05d1c0f9924a
#
####################################

import re
import os, sys
import zipfile
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

def parse_document(corpusfile, filename):
    #universal newlines does not seem to work. we need to replace the \r ourselves.
    doc = corpusfile.open(filename, 'U').read().decode(encoding='iso-8859-15').replace('\r','\n')
    result = {}
    result['title'] = find_title(doc)
    result['author'] = find_author(doc)
    result['date'] = find_date(doc)
    result['textlist'] = clean_from_nonletters(clean_from_markup(clean_from_entities(find_text(doc)))).split()
    result['text'] = clean_from_markup(clean_from_entities(find_text(doc)))
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
    text.text = doc_dict['text']
    return xml

def main(corpus, result_dir):

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    zf = zipfile.ZipFile(corpus)
    for zfile in zf.infolist():
        xml = build_xml(parse_document(zf, zfile))
        et = etree.ElementTree(xml)
        et.write(os.path.join(result_dir, zfile.filename.replace('txt', 'xml')), pretty_print=True)        
        print(zfile.filename, ' finished')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
