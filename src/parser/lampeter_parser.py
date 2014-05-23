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
    return pattern.search(content).groups()[1]

def find_text(content):
    pattern = re.compile('(<body>)(.*)(</body>)', re.IGNORECASE | re.DOTALL)
    return pattern.search(content).groups()[1]

def clean_from_nonletters(text):
    return re.sub(r'[^a-zA-Z\s]', ' ', text)

def clean_from_markup(text):
    pattern = re.compile('<.*?>', re.IGNORECASE | re.DOTALL)
    return pattern.sub('', text)

def clean_from_entities(text):
    pattern = re.compile('&[a-zA-Z]{1,5};', re.IGNORECASE)
    return pattern.sub('', text)

def parse_document(filename):
    doc = open(filename, 'r').read()
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
    out.write(str(etree.tostring(xml, pretty_print=True)))
    print(filename, ' finished')

#<xml>
#   <author>...</author>
#   <year>...</year>
#   <title>...</title>
#   <text>
#      <w>...</w>
#      ...
#   </text>
#</xml>

# Text ist im <TEXT> tag enthalten
# bereinigen von tags und entities (&rehy;, <RO>, <P>, <NOTE>, jede menge anderes)
# danach alle satzzeichen und zahlen entfernen
# split
# durchzählen und wörter mit nummern schreiben
