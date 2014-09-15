#!/usr/bin/env python3
####################################
#
# usage: ./parse_all.py <corpus_dir>
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
    for e in os.listdir(corpus_dir):
        if e[-4:] != ".zip":
            continue
        if "cen" in e:
            cen_parser.main(e, result_dir)
        if "clmet" in e:
            clmet.main(e, result_dir)
        if "ampeter" in e:
            lampeter_parser.main(e, result_dir)
        if "2507" in e:
            parse_2507.main(e, result_dir)
        if "2468" in e:
            parse_2468.main(e, result_dir)
if __name__ == "__main__":
    main(sys.argv[1])

