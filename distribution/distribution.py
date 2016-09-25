#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections.abc import MutableMapping, Mapping
from functools import reduce
import operator
import random
import statistics


def bayes_t(prior, likelihood, c):
    return (prior * likelihood) / c


def product(it):
    return reduce(operator.mul, it)


def join(*args):
    return reduce(operator.add, args)

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
            if 'joined' in kwargs:
                self.joined = kwargs.pop('joined')
            self.update(kwargs)

    def __repr__(self):
        if hasattr(self, 'name'):
            name = self.name.replace(' ', '_')
        else:
            name = self.__class__.__name__
        if not self:
            return '{}()'.format(name)
        else:
            items = ', '.join(["'{}': {}".format(k, v) for k, v in iter(self._d.items())])
            return '{}({{{}}})'.format(name, items)

    def items(self):
        return self._d.items()

    def keys(self):
        return self._d.keys()

    def values(self):
        return self._d.values()

    def sort(self, rev=True):
        return sorted(self._d.items(), key=lambda x: x[1], reverse=rev)

    def most_common(self, n=10):
        return self.sort()[:n]

    def least_common(self, n=10):
        return self.sort(rev=False)[:n]

    def P(self, item):
        return self._d.get(item, 0) / self.total()

    def Ps(self, xs):
        return [self.P(x) for x in xs]

    def sample(self, n=30):
        return random.sample(self._d.items(), n)

    def _join(*args):
        return reduce(operator.add, args)

    def __add__(self, other):
        if not isinstance(other, Distribution):
            # raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
            raise TypeError("can't add {} and {}".format(
                self.__class__.__name__, other.__class__.__name__))
        new = Distribution()
        new.update(other)
        new.update(self)
        return new

    __radd__ = __add__

    def __iadd__(self, other):
        if not isinstance(other, Distribution):
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                self.__class__.__name__, other.__class__.__name__))

        for k, v in other.items():
                self._d[k] += v
        return self

    def total(self):
        return sum(self.values())

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
        return statistics.pvariance(self._d.values())

    def std_dev(self):
        return statistics.pstdev(self._d.values())


class DistGroup(Distribution):

    def __init__(self, *args, **kwargs):
        if args:
            for arg in args[0]:
                if not isinstance(arg, Distribution):
                    raise ValueError('arguments should be Distributions')
        super().__init__(*args, **kwargs)

    def normalizer(self, item):
        joined = reduce(operator.add, self._d.keys())
        return joined.P(item)


if __name__ == "__main__":
    # cookies!
    cookies = DistGroup([Distribution(['vanilla'] * 30 + ['chocolate'] * 10, name='bowl_1'),
                         Distribution(['vanilla'] * 20 + ['chocolate'] * 20, name='bowl_2')])
    
    data = 'vanilla'
    print(max([(dist.name, cookies.P(dist) * dist.P(data) /
                cookies.normalizer(data)) for dist in cookies], key=lambda x: x[1]))
