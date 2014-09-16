#!/usr/bin/env python3
####################################
#
# usage: ./parse_2507.py <2507.zip> <output_dir>
#
####################################

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
        et.write(result_dir+"/"+zfile.filename.replace("/",""), pretty_print=True)
        #~ print(etree.tostring(et))
        print(zfile.filename, "finished")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
