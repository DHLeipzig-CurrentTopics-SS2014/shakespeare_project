#!/usr/bin/env python3
####################################
#
# usage: from parser_helpers import *
#
####################################

from lxml import etree
import string

def build_xml(year, author, title, text):
    xml = etree.Element('xml')
    author_elem = etree.SubElement(xml, 'author')
    author_elem.text = author
    year_elem = etree.SubElement(xml, 'year')
    year_elem.text = year
    title_elem = etree.SubElement(xml, 'title')
    title_elem.text = title
    text_elem = etree.SubElement(xml, 'text')
    text_elem.text = text
    et = etree.ElementTree(xml)
    return et

def write_xml_to_file(xml, file_path):
    xml.write(file_path, pretty_print=True)

# from http://stackoverflow.com/a/8735509
def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

def filter_for_xml(text):
    return ''.join(c for c in text if valid_xml_char_ordinal(c))
    #~ ''.join(filter(string.printable.__contains__, text))
