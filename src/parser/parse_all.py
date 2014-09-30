#!/usr/bin/env python3
####################################
#
# usage: ./parse_all.py <corpus_dir>
#
# <corpus_dir> must contain the following files:
# 2468.zip
# 2507.zip
# cen.zip
# clmet3_0.zip
# Lampeter_txt.zip
#
# the parsed files are stored in "<corpus_dir>/xml"
#
####################################

import lampeter_parser
import clmet
import parse_2507
import parse_2468
import cen_parser
import os, sys

def main(corpus_dir):
    result_dir = os.path.join(corpus_dir,"xml")
    cen_parser.main(os.path.join(corpus_dir, "cen.zip"), os.path.join(result_dir, "cen"))
    clmet.main(os.path.join(corpus_dir, "clmet3_0.zip"), os.path.join(result_dir, "clmet"))
    lampeter_parser.main(os.path.join(corpus_dir, "Lampeter_txt.zip"), os.path.join(result_dir, "lampeter"))
    parse_2507.main(os.path.join(corpus_dir, "2507.zip"), os.path.join(result_dir, "2507"))
    parse_2468.main(os.path.join(corpus_dir, "2468.zip"), os.path.join(result_dir, "2468"))

if __name__ == "__main__":
    main(sys.argv[1])

