#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from collections import MutableMapping
from distribution import distribution

class TestDistribution:

    def test_itialization(self):
        d1 = distribution.Distribution({'chocolate': 10, 'vanilla': 30})
        d2 = distribution.Distribution((('chocolate', 20), ('vanilla', 20)))
        d3 = distribution.Distribution(['chocolate'] * 30 + ['vanilla'] * 10)
        assert d1['chocolate'] is 10
        assert d1['vanilla'] is 30
        assert d2['vanilla'] is 20
        assert d2['chocolate'] is 20
        assert d3['vanilla'] is 10
        assert d3['chocolate'] is 30

    def test_len(self):
        d1 = distribution.Distribution({'chocolate': 10, 'vanilla': 30})
        assert len(d1) is 2

    def test_
