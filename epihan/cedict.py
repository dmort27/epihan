# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import codecs
import regex as re
import functools


class CEDict(object):
    def __init__(self, dict_file):
        self.hanzi = self._read_cedict(dict_file)
        self.every_han_char = self._get_every_han_char()
        self.isym_dict = [(x, i) for (i, x) in enumerate(self.every_han_char, 1)]
        self.every_pinyin_char = self._get_every_pinyin_char()
        self.osym_dict = [(x, i) for (i, x) in enumerate(self.every_pinyin_char, 1)]
        self.state = 0

    def _read_cedict(self, dict_file):
        comment_re = re.compile('\s*#')
        lemma_re = re.compile('(?P<hanzi>[^]]+) \[(?P<pinyin>[^]]+)\] /(?P<english>.+)/')
        cedict = {}
        with codecs.open(dict_file, 'r', 'utf-8') as f:
            for line in f:
                if comment_re.match(line):
                    pass
                elif lemma_re.match(line):
                    match = lemma_re.match(line)
                    hanzi = match.group('hanzi').split(' ')
                    pinyin = match.group('pinyin').split(' ')
                    english = match.group('english').split('/')
                    cedict[hanzi[1]] = (pinyin, english)
        return cedict

    def _get_every_han_char(self):
        return functools.reduce(lambda a, b: a | b, [set(x) for x in iter(self.hanzi)], set())

    def _get_every_pinyin_char(self):
        return functools.reduce(lambda a, b: a | b, [set(p) for (p, e) in self.hanzi.iteritems()], set())

    def symbol_table(self, table):
        text = '<eps> 0\n'
        for sym, num in sorted(table.items(), key=lambda a, b: b):
            text += '{} {}\n'.format(sym, num)

    def phrase_to_att_fst(self, phrase):
        p, e = self.hanzi[phrase]
        pairs = zip(phrase, p)
        text = ''
        for ch, pw in pairs:
            text += '{} {} {} {} 1\n'.format(self.state, self.state + 1, ch, pw[0])
            pw = pw[1:]
            self.state += 1
            for let in pw:
                text += '{} {} {} {} 1\n'.format(self.state, self.state + 1, '<eps>', let)
                self.state += 1
        text += '{} 1'.format(self.state)
        return text

    def write_hanzi_to_pinyin_fst(self, xfst):
        pass