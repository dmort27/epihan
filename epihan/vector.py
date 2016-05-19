# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import itertools
import os.path
import types
import unicodedata

import pkg_resources

import _epihan
import cedict
import panphon
import rules
import unicodecsv as csv


class VectorsWithIPASpace(_epihan.Normalizer):
    def __init__(self, cedict_file, rule_file, space_file):
        self.ft = panphon.FeatureTable()
        self.cedict = cedict.CEDictTrie(cedict_file)
        self.rules = rules.Rules([rule_file])
        self.space = self._load_ipa_space(space_file)

    def _load_space(self, space_name):
        space_fn = os.path.join('data', 'space', space_name + '.csv')
        space_fn = pkg_resources.resource_filename(__name__, space_fn)
        with open(space_fn, 'rb') as f:
            reader = csv.reader(f, encoding='utf-8')
            return {seg: num for (num, seg) in reader}

    def word_to_segs(self, word, normpunc=False):
        # Consider headwords containing capital Roman letters.
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

        def to_space(seg):
            if seg in self.space:
                return self.space[seg]
            else:
                return -1

        def hz_tuple_with_vector((case, hz, syl)):
            cats = ['L'] * len(segs)
            case = [case] + [None] * (len(syl) - 1)
            orth = [hz] + [None] * (len(syl) - 1)
            (syl, vectors) = zip(*to_vectors(syl))
            ids = map(to_space, syl)
            return zip(cats, case, orth, segs, ids, vectors)

        if normpunc:
            word = self.normalize_punc(word)
        aggregated_segs = []
        tokens = self.cedict.tokenize(word)
        for token in tokens:
            if token in self.cedict.hanzi:
                pinyin = self.cedict.hanzi[token]
                ipa = self.rules.apply(pinyin.lower())
                cat, case = cat_and_cap(pinyin[0])
                syls = ipa.split(',')
                segs = itertools.chain(map(hz_tuple_with_vector, zip(case, token, syls)))
                # output: <cat, case, orth, phon, id, vec>
            else:
                assert len(token) == 1
                [orth] = token
                cat, case = cat_and_cap(orth)
                phon = ''
                id_ = to_space[orth]
                vec = to_space(phon)
                segs = [(cat, case, orth, phon, id_, vec)]
            aggregated_segs.append(segs)
        aggregated_segs = itertools.chain(aggregated_segs)
        for seg in aggregated_segs:
            assert len(seg) == 6
            assert isinstance(seg[-1], types.ListType)
        return aggregated_segs
