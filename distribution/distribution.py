#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections.abc import MutableMapping, Mapping
import statistics
import operator
from functools import reduce

def bayes_t(prior, likelihood, c):
    return (prior * likelihood) / c


def product(it):
    return reduce(operator.mul, it) 


def invert(mapping):
    """
    invert nested mappings, e.g.:
        >>> invert({'x': {'a': 1, 'b': 2}, 'y': {'a': 2, 'b': 1}})
        {'a': {'x': 1, 'y': 2}, 'b': {'x': 2, 'y': 1}}
    """
    items = [(ik, (ok, v)) for ok, value in mapping.items() for ik, v in value.items()]
    keys = {k for k, _ in items}
    new_map = {}
    for key in keys:
        vals = []
        for k, v in items:
            if k == key:
                vals.append(v)
        new_map[key] = Distribution(dict(vals))
    return new_map


class Distribution(MutableMapping):

    def __init__(self, *args, **kwargs):
        self._d = {}
        self.update(*args, **kwargs)

    def __hash__(self):
        return id(self)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d.get(key, 0)

    def __setitem__(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError('value must be int or float')
        else:
            self._d[key] = self._d.get(key, 0) + value

    def __delitem__(self, key):
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __contains__(self, item):
        return item in self._d

    def add(self, item, val=1):
        self._d[item] = self._d.get(item, 0) + val

    def update(self, *args, **kwargs):
        if args:
            it = args[0]
            if isinstance(it, Mapping):
                for k, v in it.items():
                    self.add(k, v)
            elif it and isinstance(it, (list, tuple)) and isinstance(it[0], tuple):
                for k, v in it:
                    self.add(k, v)
            elif isinstance(it, (list, tuple)):
                for k in it:
                    self.add(k)
            else:
                self.add(it)

        if kwargs:
            if 'name' in kwargs:
                self.name = kwargs.pop('name')
            self.update(kwargs)

    def __repr__(self):
        name = self.__class__.__name__
        if not self:
            return '{}()'.format(name)
        else:
            items = ', '.join(["('{}', {})".format(k, v) for k, v in iter(self._d.items())])
            return '{}(({}))'.format(name, items)

    def items(self):
        return self._d.items()

    def keys(self):
        return self._d.keys()

    def values(self):
        return self._d.values()

    def total(self):
        return sum(self.values())

    def __add__(self, other):
        if not isinstance(other, Distribution):
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                self.__class__.__name__, other.__class__.__name__))

        self.update(other)
        return Distribution(self)

    __radd__ = __add__

    def __iadd__(self, other):
        if not isinstance(other, Distribution):
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                self.__class__.__name__, other.__class__.__name__))

        for k, v in other.items():
                self._d[k] += v
        return self

    def sort(self, rev=True):
        return sorted(self._d.items(), key=lambda x: x[1], reverse=rev)

    def most_common(self, n=10):
        return self.sort()[:n]

    def least_common(self, n=10):
        return self.sort(rev=False)[:n]

    def normalize(self):
        total = self.total()
        f = 1 / total
        normalized = Distribution()
        for k, v in self._d.items():
            normalized[k] = v * f
        return normalized

    def mean(self):
        n = len(self._d)
        return self.total() / n

    def median(self):
        l = self.sort()
        middle = len(l) // 2
        start = l[:middle]
        end = l[middle:]
        if len(l) % 2 == 0:
            return (start[-1][1] + end[0][1]) / 2
        else:
            return l[middle][1]

    def mode(self):
        return max(self._d.items(), key=lambda x: x[1])

    def variance(self):
        # return sum([(v - self.mean())**2 for v in self._d.values()]) / len(self._d)
        return statistics.pvariance(self._d.values())

    def std_dev(self):
        return statistics.pstdev(self._d.values())

    def P(self, item):
        return self._d.get(item, 0) / self.total()


if __name__ == "__main__":
    # cookies!
    # bowl1 = Distribution(['vanilla'] * 30 + ['chocolate'] * 10, name='bowl 1')
    # bowl2 = Distribution(['vanilla'] * 20 + ['chocolate'] * 20, name='bowl 2')

    # suite = Distribution([bowl1, bowl2])
    # for dist in suite:
    #     print('{}: {}'.format(dist.name, bayes_t(suite.P(dist),
    #                                              dist.P('vanilla'),
    #                                              (sum(d.P('vanilla') for d in
    #                                                   suite) / 2))))

    # mnms
    pre_95 = Distribution(brown=.3, yellow=.2, red=.2, green=.1, orange=.1,
                          tan=.1, name='pre_95')
    post_95 = Distribution(blue=.24, green=.20, orange=.16, yellow=.14,
                           red=.13, brown=.13, name='post_95')
    
    bags = Distribution([pre_95, post_95])

    # there are 2 bags, one from 1994 and one from 1996. You pick two m&ms, a
    # yellow and a green one. the yellow m&m came from bag 1.
    # What is the probability that bag 1 is from 1994?
    # hypotheses:
    #   A: bag 1 is pre_95, bag 2 is post 95
    #   B: bag 1 is post_95, bag 2 is pre 95

        # prior   likelihood    p*lh    posterior
    # --  -----   ------------  ----    ---------
    # A     .5    y:.2 * g:.2   .02    .02/.027
    # B     .5    y:.14 * g:.1  .007    .007/.027

    # hypo_A = ('A', bags.P(pre_95), pre_95.P('yellow'), post_95.P('green'))
    # hypo_B = ('B', bags.P(post_95), post_95.P('yellow'), pre_95.P('green')) 

    # def posterior(hypos):
    #     c = sum([product(h[1:]) for h in hypos])
    #     for h in hypos:
    #         name, *ps = h
    #         print(name, product(ps)/c)


    # posterior([hypo_A, hypo_B])
