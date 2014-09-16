#!/usr/bin/env python3
####################################
#
# usage: ./parse_2468.py <2468.zip> <output_dir>
#
####################################

import codecs
import re
import sys, os
import zipfile

# CONVERT ORFORD ANNOTATED FILES TO XML (2468.zip/orford.txt)

def interp(text, author, year, cnt, result_dir):
    text = re.sub(r'[%=&\"\'\^\.,\{\}~:£\*\(\)_\-\;\?0-9<>]+', "", text)
    text = re.sub(r'\s+', " ", text)
    output = "<xml>\n"  # cheap xml generator, sorry, I'm lazy
    output += "  <author>"+author.strip()+"</author>\n"
    output += "  <year>"+year.strip()+"</year>\n"
    output += "  <title>Letter "+str(cnt)+" from"+author+" in"+year+"</title>\n"
    output += "  <text>\n"
    for w in text.split():
        if w not in ["st", "nd", "rd", "th"]: # no numbers
            output += w+" "
    output += "  </text>\n"
    output += "</xml>"
    with open(result_dir + "/letter"+str(cnt)+".xml", "w") as f:
        f.write(output)
    print(cnt)

def main(corpus, result_dir):

    #~ corpus = sys.argv[1]
    #~ result_dir = sys.argv[2]

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    zf = zipfile.ZipFile(corpus)

    orford = zf.open("2468/orford.txt", "r").read().decode("ISO-8859-15")

    fsm = 0 #finite state machine
    text = ""
    author = ""
    year = "" # could be an Integer, but who cares?
    cnt = 0

    for char in orford:
        if fsm == 4: # ignore tag
            if char == '>':
                fsm = 0 # set ready mode

        elif fsm == 3: # year mode
            if char == '>' or len(year) == 5:
                fsm = 0 # set ready mode
            elif char == '?':
                pass
            else:
                year += char

        elif fsm == 2: # author mode
            if char == '>':
                cnt += 1
                interp(text, author, year, cnt, result_dir)
                text = ""
                fsm = 0 # set ready mode
            else:
                author += char

        elif fsm == 1 and char.lower() == 'a': # tag mode
            fsm = 2
            author = ""

        elif fsm == 1 and char.lower() == 'o': # tag mode
            fsm = 3
            year = ""

        elif fsm == 1 and char.lower() == 'p': # tag mode
            fsm = 4

        elif fsm == 1:
            fsm = 0 # tag mode timeout

        elif fsm == 0 and char == '<': # ready mode
            fsm = 1

        elif fsm == 0 and char == '[':
            fsm = 5

        elif fsm == 5 and char == '^':
            fsm = 6

        elif fsm == 6:
            if char == '^':
                fsm = 7

        elif fsm == 7:
            if char == ']':
                fsm = 0
            else:
                fsm = 6

        else:
            text += char

    interp(text, author, year, cnt, result_dir)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
