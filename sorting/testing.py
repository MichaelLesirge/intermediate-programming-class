import unittest

import algorithms
from util import make_random

class TestLinkedList(unittest.TestCase):
    def assert_all_sorted(self, array: list):
        sorted_array = sorted(array)
        for algorithm in algorithms.__all__:
            array_copy = array.copy()
            algorithm(array_copy)
            self.assertEqual(array_copy, sorted_array, f"Failed algorithm: {algorithm.__name__}")
    
    def test_empty(self):
        self.assert_all_sorted(make_random(0))

    def test_one_long(self):
        self.assert_all_sorted(make_random(1))

    def test_two_long(self):
        self.assert_all_sorted(make_random(2))
            
    def test_long(self):
        self.assert_all_sorted(make_random(100))
            
    def test_bumpy_long(self):
        self.assert_all_sorted(make_random(100, num_range=(0, 1000)))
            
    def test_negative_long(self):
        self.assert_all_sorted(make_random(20, num_range=(-100, 100)))

if __name__ == '__main__':
    unittest.main()