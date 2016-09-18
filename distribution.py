#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


class Distribution(Counter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._normalized = {}
        self._updated = False

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._updated = True

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def normalized(self):
        if (not self._normalized) or self._updated:
            total = sum(self.values())
            for k, v in self.items():
                self._normalized[k] = v / total
        self._updated = False
        return self._normalized

    def P(self, key):
        return self.normalized().get(key, 0)

    def __repr__(self):
        name = self.__class__.__name__
        items = ', '.join(["('{}', {})".format(k, v) for k, v in iter(self.items())])
        return '{}({})'.format(name, items)


if __name__ == "__main__":

    x = Distribution({'vanilla': 20, 'chocolate': 20})
    bowl = ['vanilla'] * 10 + ['chocolate'] * 20
    y = Distribution(bowl)
    y.update(x)
    for k in y:
        print(k, y[k], y.P(k))
