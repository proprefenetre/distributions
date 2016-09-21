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
        self.update(*args, **kwargs)

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__.get(key, 0)

    def __setitem__(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError('value must be int or float')
        else:
            self.__dict__[key] = self.__dict__.get(key, 0) + value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def update(self, *args, **kwargs):
        d = self.__dict__
        if args:
            if isinstance(args[0], Mapping):
                for k, v in args[0].items():
                    d[k] = d.get(k, 0) + v
            else:
                for k in args:
                    d[k] = d.get(k, 0) + 1
        if kwargs:
            for k, v in kwargs.items():
                d[k] = d.get(k, 0) + v

    def __hash__(self):
        return id(self)

    def __repr__(self):
        name = self.__class__.__name__
        if not self:
            return '{}()'.format(name)
        else:
            items = ', '.join(["('{}', {})".format(k, v) for k, v in iter(self.__dict__.items())])
            return '{}({})'.format(name, items)

    def __add__(self, other):
        new = Distribution(self.__dict__)
        if isinstance(other, Distribution):
            new.update(other)
            return new
        else:
            raise TypeError

if __name__ == "__main__":

    b1 = Distribution('bowl 1', {'chocolate': 10, 'vanilla': 30})
    b2 = Distribution('bowl 2', {'chocolate': 20, 'vanilla': 20})
