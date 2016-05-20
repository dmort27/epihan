#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import epihan.vector
import lxml.etree as etree
import argparse
import types
import codecs

def main(ltf_files):
    v = epihan.vector.VectorsWithIPASpace('cedict', 'pinyin-to-ipa', 'zh-Han')
    for ltf_file in ltf_files:
        tree = etree.parse(ltf_file)
        root = tree.getroot()
        for token in root.iter('TOKEN'):
            text = unicode(token.text)
            print('text={}'.format(text))
            print(v.word_to_segs(text))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', help='Input file (LTF)')
    args = parser.parse_args()
    main(args.input)
