#!/usr/bin/env python3
####################################
#
# usage: ./clmet.py <clmet3_0.zip> <output_dir>
#
# SHA256 (clmet3_0.zip) = e84ecaca60513c267852d28a9dde2f60a5044d44a7b7c1c33f1397604bb0be19
# MD5 (clmet3_0.zip) = 5357ef3a13b7502797fee0bb0edc2aec
#
####################################

from lxml import etree
from os import makedirs
from os.path import join,exists
import sys
import zipfile
from parser_helpers import *

def main(corpus, result_dir):
    if not exists(result_dir): makedirs(result_dir)

    zf = zipfile.ZipFile(corpus)
    for e in zf.infolist():
        if e.filename.startswith("plain_text/") and e.file_size > 0:
            xml=etree.parse(zf.open(e),parser=etree.HTMLParser(encoding='latin2'))
            author = xml.xpath("//author")[0].xpath("string()")
            title = xml.xpath("//title")[0].xpath("string()")
            year = xml.xpath("//date")[0].xpath("string()")

            text = xml.xpath("//text")[0].xpath("string()")

            xml = build_xml(year, author, title, text)
            write_xml_to_file(xml, join(result_dir,e.filename.replace('/', '') + ".xml"))

            print(e.filename, "finished")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
