#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from collections import Counter
from collections.abc import MutableMapping, Mapping
# import operator
# import functools


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

    def update(self, *args, **kwargs):
        if args:
            it = args[0]
            if isinstance(it, Mapping):
                for k, v in it.items():
                    self._d[k] = self._d.get(k, 0) + v
            elif it and isinstance(it, (list, tuple)) and isinstance(it[0], tuple):
                for k, v in it:
                    self._d[k] = self._d.get(k, 0) + v
            else:
                for k in it:
                    self._d[k] = self._d.get(k, 0) + 1
        if kwargs:
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
        self._total = sum(self.values())
        return self._total

    def __add__(self, other):
        if isinstance(other, Distribution):
            self.update(other)
            return Distribution(self)
        else:
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                self.__class__.__name__, other.__class__.__name__))

    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Distribution):
            for k, v in other.items():
                    self._d[k] += v
            return self
        else:
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                self.__class__.__name__, other.__class__.__name__))

    def sort(self, rev=True):
        return sorted(self._d.items(), key=lambda x: x[1], reverse=rev)

    def normalize(self):
        total = self.total()
        f = 1 / total
        for k in self._d:
            self._d[k] *= f

    def most_common(self, n=10):
        pass

    def most_likely(self, n=10):
        pass




if __name__ == "__main__":
    from pathlib import Path

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

    text = get_books()
    corpus = Distribution([s.strip('.,!?\'" ') for s in ' '.join(text).split()])
    corpus.normalize()
    print(corpus.sort(False))
