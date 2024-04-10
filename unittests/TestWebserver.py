import unittest
import os
import sys

current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir, '..', 'app')
sys.path.append(app_dir)

from data_ingestor import DataIngestor

class TestWebserver(unittest.TestCase):

    def test_states_mean(self):
        """
        Test case for the states_mean method of the DataIngestor class.
        It checks if the calculated mean value matches the expected value from the input file.
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/states_mean.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.states_mean(question)())

    def test_state_mean(self):
        """
        Test case for the state_mean method of the DataIngestor class.

        This test verifies that the state_mean method returns the expected result
        when given a specific question and state.

        The test reads the expected result from a JSON file and compares it with
        the actual result returned by the state_mean method.

        Test Input:
        - question: "Percent of adults aged 18 years and older who have an overweight
        classification"
        - state: "Wisconsin"

        Expected Output:
        - The expected result is read from the "unittests/input/state_mean.json" file.

        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_mean.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.state_mean(question, state)())

    def test_best5(self):
        """
        Test case for the best5 method of the DataIngestor class.

        This test case verifies that the best5 method returns the expected result
        when given a specific question and input data.

        The test reads the expected output from a JSON file and compares it with
        the actual output of the best5 method. The test passes if the two outputs
        match, and fails otherwise.
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/best5.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.best5(question)())

    def test_worst5(self):
        """
        Test case for the worst5 method of the DataIngestor class.
        It checks if the output of the worst5 method matches the content of the 'worst5.json' file.
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/worst5.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.worst5(question)())

    def test_global_mean(self):
        """
        Test case for the global_mean method of the DataIngestor class.
        It checks if the calculated global mean matches the expected value.

        Returns:
            None
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/global_mean.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.global_mean(question)())

    def test_diff_from_mean(self):
        """
        Test case for the `d_iff_from_mean` method of the DataIngestor class.
        It checks if the output of the method matches the expected result.

        Returns:
            None
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/diff_from_mean.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.diff_from_mean(question)())

    def test_state_diff_from_mean(self):
        """
        Test case for the state_d_iff_from_mean method of the DataIngestor class.
        It checks if the calculated value matches the expected value read from a JSON file.
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_diff_from_mean.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.state_diff_from_mean(question, state)())

    def test_mean_by_category(self):
        """
        Test case for the mean_by_category method of the DataIngestor class.
        It checks if the calculated mean by category matches the expected result.

        Returns:
            None
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        with open("unittests/input/mean_by_category.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.mean_by_category(question)())

    def test_state_mean_by_category(self):
        """
        Test case for the state_mean_by_category method of the DataIngestor class.
        It checks if the method returns the expected result by comparing the output
        with the contents of a JSON file.

        Returns:
            None
        """
        d_i = DataIngestor("unittests/test.csv")
        question = "Percent of adults aged 18 years and older who have an overweight classification"
        state = "Wisconsin"
        with open("unittests/input/state_mean_by_category.json", "r", encoding='utf-8') as f_in:
            self.assertEqual(f_in.read(), d_i.state_mean_by_category(question, state)())

    if __name__ == '__main__':
        unittest.main()
