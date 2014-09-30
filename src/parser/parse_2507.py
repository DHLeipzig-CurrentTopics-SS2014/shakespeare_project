#!/usr/bin/env python3
####################################
#
# usage: ./parse_2507.py <2507.zip> <output_dir>
#
# SHA256 (2507.zip) = a9dff6244fe74881099c576cc7ab32ddd86d3b8bee2e44da94938742b4f32154
# MD5 (2507.zip) = f8b1442d18fd72cfa84abad3ed3c48b5
#
####################################

from parser_helpers import *
from lxml import etree
import os
import glob
import sys
import zipfile
import io

def main(corpus, result_dir):

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    parser = etree.XMLParser()

    with zipfile.ZipFile(corpus) as z:
        with z.open("2507/CEDXML.ZIP") as z2:
            z2_filedata = io.BytesIO(z2.read())
            zf = zipfile.ZipFile(z2_filedata)
    for zfile in zf.infolist():
        if zfile.filename[-4:] != ".xml":
            continue
        doc = etree.parse(zf.open(zfile.filename), parser)
        #~ print(etree.tostring(root))#, pretty_print=True))
        root = doc.getroot()

        # Author
        author = root.xpath("dialogueHeader/author")[0].text

        # Year
        year = root.xpath("dialogueHeader/speechPubDate")[0].text.split()[1].split("/")[0].split("-")[0]

        # Title
        title = root.xpath("dialogueHeader/title")[0].text

        # Text
        text_string = ""
        for dialogue in root.iter("dialogue"):
            for dChild in dialogue:
                if "comment" == dChild.tag:
                    dialogue.text += dChild.tail
                    dialogue.remove(dChild)

            text_string += " " + dialogue.xpath("string()")

        write_xml_to_file(build_xml(year, author, title, text_string), os.path.join(result_dir, zfile.filename.replace("/","")))
        print(zfile.filename, "finished")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
