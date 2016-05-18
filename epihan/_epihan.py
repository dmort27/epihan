# -*- utf-8 -*-
from __future__ import print_function, unicode_literals

import os.path

import pkg_resources

import cedict
import rules


class Normalizer(object):

    def normalize_punc(self, text):
        punc = [(u'\uff0c', u','),
                (u'\uff01', u'!'),
                (u'\uff1f', u'?'),
                (u'\uff1b', u';'),
                (u'\uff1a', u':'),
                (u'\uff08', u'('),
                (u'\uff09', u')'),
                (u'\uff3b', u'['),
                (u'\uff3d', u']'),
                (u'\u3010', u'['),
                (u'\u3011', u']'),
                ]
        for a, b in punc:
            text = text.replace(a, b)
        return text


class Epihan(Normalizer):
    def __init__(self, cedict_file, rules_file):
        path = os.path.join('data', cedict_file + '.txt')
        cedict_file = pkg_resources.resource_filename(__name__, path)
        path = os.path.join('data', rules_file + '.txt')
        rules_file = pkg_resources.resource_filename(__name__, path)
        self.cedict = cedict.CEDictTrie(cedict_file)
        self.rules = rules.Rules([rules_file])

    def transliterate(self, text, normpunc=False):
        tokens = self.cedict.tokenize(text)
        ipa_tokens = []
        for token in tokens:
            if token in self.cedict.hanzi:
                (pinyin, _) = self.cedict.hanzi[token]
                pinyin = ''.join(pinyin)
                ipa = self.rules.apply(pinyin)
                ipa_tokens.append(ipa.replace(',', ''))
            else:
                if normpunc:
                    token = self.normalize_punc(token)
                ipa_tokens.append(token)
        return ''.join(ipa_tokens)
