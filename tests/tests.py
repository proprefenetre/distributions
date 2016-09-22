#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from collections import MutableMapping
from distribution.distribution import Distribution


b1 = Distribution({'chocolate': 10, 'vanilla': 30})
b2 = Distribution((('chocolate', 20), ('vanilla', 20)))
b3 = Distribution(chocolate=30, vanilla=10)


class TestDistribution(unittest.TestCase):

    def test_self(self):
        self.assertIsInstance(b1, MutableMapping, 'not instance of MutableMapping')
        self.assertIsInstance(b2, MutableMapping, 'not instance of MutableMapping')
        self.assertIsInstance(b3, MutableMapping, 'not instance of MutableMapping')

    def test_frequency(self):
        self.assertEqual(b1['chocolate'], 10)
        self.assertEqual(b2['vanilla'], 20)

    def test_total(self):
        self.assertEqual(b1.total(), 40)
        self.assertEqual(b2.total(), 40)
        self.assertEqual(b3.total(), 40)

if __name__ == '__main__':
    unittest.main()
