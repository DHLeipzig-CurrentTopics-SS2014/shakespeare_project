#!/usr/bin/env python3
####################################
#
# usage: ./clmet.py <clmet3_0.zip> <output_dir>
#
####################################

from lxml import etree
from os import makedirs
from os.path import join,exists
import sys
import zipfile

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
            file = open(join(result_dir,e.filename.replace('/', '') + ".xml"),"w")
            file.write("<xml>")

            file.write("<author>"+author+"</author>");
            file.write("<year>"+year+"</year>");
            file.write("<title>"+title+"</title>")


            file.write("<text>")
            file.write(text)
            file.write("</text>")
            file.write("</xml>")
            file.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
