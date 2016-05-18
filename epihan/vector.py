# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import unicodedata

import itertools
import panphon
import cedict
import rules
import _epihan


class VectorsWithIPASpace(_epihan.Normalizer):
    def __init__(self, cedict_file, rule_file, space_file):
        self.ft = panphon.FeatureTable()
        self.cedict = cedict.CEDictTrie(cedict_file)
        self.rules = rules.Rules([rule_file])
        self.space = self._load_ipa_space(space_file)

    def _load_ipa_space(self, space_file):
        pass

    def word_to_segs(self, word, normpunc=False):

        def cat_and_cap(c):
            cat, case = tuple(unicodedata.category(c))
            case = 1 if case == 'u' else 0
            return unicode(cat), case

        def recode_ft(ft):
            if ft == '+':
                return 1
            elif ft == '0':
                return 0
            elif ft == '-':
                return -1

        def vec2bin(vec):
            return map(recode_ft, vec)

        def to_vector(seg):
            return seg, vec2bin(self.ft.segment_to_vector(seg))

        def to_vectors(phon):
            if phon == u'':
                return [(-1, [0] * self.num_panphon_fts)]
            else:
                return [to_vector(seg) for seg in self.ft.segs(phon)]

        def hz_vector((hz, syl)):
            (segs, vectors) = zip(*to_vectors(syl))
            hz_padded = [hz] + [''] * (len(segs) - 1)
            return zip(hz_padded, segs, vectors)

        if normpunc:
            word = self.normalize_punc(word)
        aggregated_segs  = []
        tokens = self.cedict.tokenize(word)
        for token in tokens:
            if token in self.cedict.hanzi:
                pinyin = self.cedict.hanzi[token]
                ipa = self.rules.apply(pinyin.lower())
                cat, cap = cap_and_cap(pinyin[0])
                syls = ipa.split(',')
                segs = itertools.chain(map(hz_vector, zip(token, syls)))
            else:
                pass
            aggregated_segs.append(segs)
        aggregated_segs = itertools.chain(aggregated_segs)
