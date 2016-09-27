#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribution import distribution
from pathlib import Path
import statistics

d1 = distribution.Distribution({'chocolate': 10, 'vanilla': 30})
d2 = distribution.Distribution((('chocolate', 20), ('vanilla', 20)))
d3 = distribution.Distribution(['chocolate'] * 30 + ['vanilla'] * 10)


def get_books(n=0):
    data_dir = Path('/home/niels/projects/python/bouquet/data')
    books = [b for b in data_dir.glob('*/*') if b.suffix == '.txt']
    text = []
    if n > len(books):
        print('{} books available, using all books'.format(len(books)))
    for idx, book in enumerate(books):
        if n > 0 and idx >= n:
            break
        else:
            with book.open() as f:
                text.append(f.read())
    return text


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

    def test_mean(self):
        text = get_books(3)
        frequency = distribution.Distribution([s.strip('.,!?\'" ') for s in ' '.join(text).split()])
        assert frequency.mean() == statistics.mean(frequency.values())

    def test_median(self):
        text = get_books(3)
        frequency = distribution.Distribution([s.strip('.,!?\'" ') for s in ' '.join(text).split()])
        assert frequency.median() == statistics.median(frequency.values())

    def test_variance(self):
        text = get_books(3)
        frequency = distribution.Distribution([s.strip('.,!?\'" ') for s in ' '.join(text).split()])
        assert frequency.variance() == statistics.pvariance(frequency.values())


class TestDistGroup:

    def test_cookie_problem(self):
        bowl_1 = distribution.Distribution(['vanilla'] * 30 + ['chocolate'] * 10, name='bowl_1')
        bowl_2 = distribution.Distribution(['vanilla'] * 20 + ['chocolate'] * 20, name='bowl_2')

        # given these two bowls, what is the chance that a vanilla cookie comes
        # from bowl_1?

        cookies = distribution.DistGroup([bowl_1, bowl_2])
        data = 'vanilla'
        cookies.normalize()
        probabilities = dict([(dist.name, (cookies.P(dist) * dist.P(data)) / cookies.normalizer(data)) for dist in cookies])
        assert cookies.P('bowl_1') == 0.5, "prior probs are wrong"
        assert cookies.normalizer(data) == 0.625, "overall prob is wrong"
        assert len(probabilities) == 2, "not all distributions are present"
        assert probabilities['bowl_1'] == 0.6, "probability for bowl_1 should be 0.6"
        assert probabilities['bowl_2'] == 0.4, "probability for bowl_2 should be 0.4"

    def test_monty_hall(self):
        door_A = distribution.Distribution(name='A')
        door_B = distribution.Distribution(name='B')
        door_C = distribution.Distribution(name='C')
        dists = distribution.DistGroup()

