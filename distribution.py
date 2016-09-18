#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter


class Distribution(Counter):

    def normalized(self):
        total = sum(self.values())
        normalized = {}
        for k, v in self.items():
            normalized[k] = v / total
        return normalized

    def __repr__(self):
        name = self.__class__.__name__
        items = ', '.join(["('{}', {})".format(k, v) for k, v in iter(self.items())])
        return '{}({})'.format(name, items)


if __name__ == "__main__":

    x = Distribution({'vanilla': 20, 'chocolate': 20})
    bowl = [('vanilla', 10), ('chocolate', 20)]
    y = Distribution()
    for k, v in bowl:
        y[k] = v

    print(y.normalized())
    y.update(x)
    print(y)
    print(y.normalized())
