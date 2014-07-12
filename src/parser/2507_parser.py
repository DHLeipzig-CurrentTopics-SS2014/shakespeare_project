#!/usr/bin/python3
####################################
#
# usage: ./2507_parser.py <input_dir> <output_dir>
#
# input_dir:
#     directory that contains xml files ( "CEDXML" )
#
####################################

from lxml import etree
import os
import glob
import sys

input_dir = sys.argv[1]
result_dir = sys.argv[2]

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

parser = etree.XMLParser()

for docFile in os.listdir(input_dir):
    if docFile[-4:] != ".xml":
        continue
    doc = etree.parse(input_dir+"/"+docFile, parser)
    root = doc.getroot()

    resultDoc = etree.ElementTree()
    rRoot = etree.Element("xml")

    # Author
    authorElement = etree.Element("author")
    authorElement.text = root.xpath("dialogueHeader/author")[0].text
    rRoot.append(authorElement)
    
    # Year
    yearElement = etree.Element("year")
    yearElement.text = root.xpath("dialogueHeader/speechPubDate")[0].text.split()[1].split("/")[0].split("-")[0]
    rRoot.append(yearElement)

    # Title
    titleElement = etree.Element("title")
    titleElement.text = root.xpath("dialogueHeader/title")[0].text
    rRoot.append(titleElement)

    # Text
    
    text_strings = []
    for dialogue in root.iter("dialogue"):
        for dChild in dialogue:
            if "comment" == dChild.tag:
                dialogue.text += dChild.tail
                dialogue.remove(dChild)

        text_strings += dialogue.xpath("string()").split()
    
    text_elem = etree.Element("text")
    text_elem.text = " ".join(text_strings)
    rRoot.append(text_elem)

    et = etree.ElementTree(rRoot)
    et.write(result_dir+"/"+docFile, pretty_print=True)
    #~ print(etree.tostring(et))
    
