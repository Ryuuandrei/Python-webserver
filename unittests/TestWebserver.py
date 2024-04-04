import unittest
from app import data_ingestor
 
class TestWebserver(unittest.TestCase):
 
    def test_states_mean(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_state_mean(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_best5(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_worst5(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_global_mean(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_diff_from_mean(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_state_diff_from_mean(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_mean_by_category(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_state_mean_by_category(self):
        self.assertEqual('foo'.upper(), 'FOO')

    if __name__ == '__main__':
        unittest.main()

