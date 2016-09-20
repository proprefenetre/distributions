#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import operator
import functools


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


class Distribution(Counter):

    def __init__(self, name=None, *args, **kwargs):
        self._normalized = [False, {}]
        self.name = name 
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return id(self)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._normalized[0] = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._normalized[0] = True

    def normalized(self):
        state, content = self._normalized
        if (not state) or (not content):
            total = sum(self.values())
            for k, v in self.items():
                content[k] = v / total
        state = True
        self._normalized = state, content
        return content

    def P(self, key):
        return self.normalized().get(key, 0)

    def __repr__(self):
        name = self.__class__.__name__
        items = ', '.join(["('{}', {})".format(k, v) for k, v in iter(self.items())])
        return '{}({})'.format(name, items)


class Suite(Distribution):

    def P(self, key):
        for k, v in self.normalized().items():
            if k.name == key:
                return v

    def hypo(self, h):
        for k in self:
            if k.name == h:
                return k

    def joined(self):
        x = Distribution()
        x.update(functools.reduce(operator.add, self.keys()))
        return x

    def normalizer(self, key):
        return self.joined().P(key)

if __name__ == "__main__":

    b1 = Distribution('bowl 1', {'chocolate': 10, 'vanilla': 30})
    b2 = Distribution('bowl 2', {'chocolate': 20, 'vanilla': 20})
    
    bs = Suite('bowls')
    bs.update([b1, b2])

    D = 'vanilla'
    H = 'bowl 1'
    print((bs.P(H) * bs.hypo(H).P(D)) / bs.normalizer(D))
    print()

