import argparse
import codecs
import logging
from collections import Counter

import epihan
import panphon
import unicodecsv as csv

logging.basicConfig(level=logging.WARNING)


def normpunc(epi, s):
    def norm(c):
        if c in dict(epi.punc):
            return epi.normalize_punc(c)
        else:
            return c
    return ''.join(map(norm, s))


def add_record_gen(epi, ft, orth):
    space = Counter()
    orth = normpunc(epi, orth)
    trans = epi.transliterate(orth)
    while trans:
        pref = ft.longest_one_seg_prefix(trans)
        if pref != '':
            space[pref] += 1
            trans = trans[len(pref):]
        else:
            if trans[0] in epi.puncnorm_vals:
                space[trans[0]] += 1
            else:
                space[trans[0]] += 1
            trans = trans[1:]
    return space


def add_file(epi, ft, fn):
    space = Counter()
    with codecs.open(fn, 'r', 'utf-8') as f:
        for line in f:
            fields = line.split(u'\t')
            if len(fields) > 0:
                orth = fields[0]
                space.update(add_record_gen(epi, ft, orth))
    logging.debug(u'Length of counter:\t{}'.format(len(space)))
    return space


def print_space(output, space):
    pairs = enumerate(sorted(filter(lambda x: x, space.keys())))
    with open(output, 'wb') as f:
        writer = csv.writer(f, encoding='utf-8')
        for i, char in pairs:
            writer.writerow((i, char))


def main(infiles, output):
    epi = epihan.Epihan('cedict', 'pinyin-to-ipa')
    ft = panphon.FeatureTable()
    space = Counter()
    for fn in infiles:
        logging.debug(u'Scanning:\t{}'.format(fn).encode('utf-8'))
        space.update(add_file(epi, ft, fn))
    print_space(output, space)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Output file.')
    parser.add_argument('infiles', nargs='+', help='CONLL files serving as basis for segment space.')
    args = parser.parse_args()
    main(args.infiles, args.output)
