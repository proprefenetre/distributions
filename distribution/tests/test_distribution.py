#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribution import distribution

d1 = distribution.Distribution({'chocolate': 10, 'vanilla': 30})
d2 = distribution.Distribution((('chocolate', 20), ('vanilla', 20)))
d3 = distribution.Distribution(['chocolate'] * 30 + ['vanilla'] * 10)

pd1 = distribution.ProbDistribution({'chocolate': 10, 'vanilla': 30})
pd2 = distribution.ProbDistribution((('chocolate', 20), ('vanilla', 20)))
pd3 = distribution.ProbDistribution(['chocolate'] * 30 + ['vanilla'] * 10)

class TestDistribution:

    def test_itialization(self):
        assert d1['vanilla'] is 30
        assert d2['vanilla'] is 20
        assert d3['vanilla'] is 10

    def test_len(self):
        assert len(d1) is 2
        assert len(d2) is 2
        assert len(d3) is 2

    def test_update(self):
        new = d1
        new.update(d2)
        assert new['chocolate'] is 30


class TestProbDist:

    def test_itialization(self):
        assert pd1['chocolate'] == 0.25
        assert pd2['chocolate'] == 0.5
        assert pd3['chocolate'] == 0.75
