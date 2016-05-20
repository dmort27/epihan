#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import epihan.vector
import lxml.etree as etree
import argparse

def main(ltf_file):
    v = epihan.vector.VectorsWithIPASpace('cedict', 'pinyin-to-ipa', 'zh-Han')
    tree = etree.parse(ltf_file)
    root = tree.getroot()
    for token in root.iter('TOKEN'):
        print(v.word_to_segs(token.text))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file (LTF)')
    args = parser.parse_args()
    main(args.input)
