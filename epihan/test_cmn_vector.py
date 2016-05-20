#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import unittest

import vector


class TestPinyin(unittest.TestCase):
    def setUp(self):
        self.v = vector.VectorsWithIPASpace('cedict', 'pinyin-to-ipa', 'cmn-Han')

    def _tuples_to_pinyin(self, tuples):
        return ''.join(map(lambda t: t[3], tuples))

    def _hz_to_pinyin(self, hz):
        py = self._tuples_to_pinyin(self.v.word_to_segs(hz))
        print('pinyin={}'.format(py))
        return py

    def test_initials(self):
        self.assertEqual('pʰjan', self._hz_to_pinyin('片'))
        self.assertEqual('pjan', self._hz_to_pinyin('变'))
        self.assertEqual('mjan', self._hz_to_pinyin('面'))
        self.assertEqual('t͡ɕʰjan', self._hz_to_pinyin('前'))
        self.assertEqual('t͡ɕjan', self._hz_to_pinyin('间'))
        self.assertEqual('ʈ͡ʂʐ̩', self._hz_to_pinyin('之'))
        self.assertEqual('ʈ͡ʂʰʐ̩', self._hz_to_pinyin('吃'))

    def test_medials(self):
        self.assertEqual('xwa', self._hz_to_pinyin('花'))
        self.assertEqual('y', self._hz_to_pinyin('鱼'))
        self.assertEqual('u', self._hz_to_pinyin('五'))
        self.assertEqual('i', self._hz_to_pinyin('一'))
        self.assertEqual('waŋ', self._hz_to_pinyin('王'))
        self.assertEqual('ɥɛn', self._hz_to_pinyin('元'))

    def test_codas(self):
        self.assertEqual('piŋ', self._hz_to_pinyin('冰'))
        self.assertEqual('pin', self._hz_to_pinyin('宾'))
        self.assertEqual('aɻ', self._hz_to_pinyin('二'))
