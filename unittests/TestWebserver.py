import unittest
import os
import sys

current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, '..', 'app')
sys.path.append(app_dir)

from data_ingestor import DataIngestor
 
class TestWebserver(unittest.TestCase):
 
    def test_states_mean(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/states_mean.json", "r") as f:
            self.assertEqual(f.read(), di.states_mean(question)())

    def test_state_mean(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_mean.json", "r") as f:
            self.assertEqual(f.read(), di.state_mean(question, state)())

    def test_best5(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/best5.json", "r") as f:
            self.assertEqual(f.read(), di.best5(question)())

    def test_worst5(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/worst5.json", "r") as f:
            self.assertEqual(f.read(), di.worst5(question)())

    def test_global_mean(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/global_mean.json", "r") as f:
            self.assertEqual(f.read(), di.global_mean(question)())

    def test_diff_from_mean(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/diff_from_mean.json", "r") as f:
            self.assertEqual(f.read(), di.diff_from_mean(question)())

    def test_state_diff_from_mean(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_diff_from_mean.json", "r") as f:
            self.assertEqual(f.read(), di.state_diff_from_mean(question, state)())

    def test_mean_by_category(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/mean_by_category.json", "r") as f:
            self.assertEqual(f.read(), di.mean_by_category(question)())

    def test_state_mean_by_category(self):
        di = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_mean_by_category.json", "r") as f:
            self.assertEqual(f.read(), di.state_mean_by_category(question, state)())

    if __name__ == '__main__':
        unittest.main()

