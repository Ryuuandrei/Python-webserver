import os
import json
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def states_mean(self, question: str):
        """
        Calculate the mean of the 'Data_Value' column for a given question, grouped by 'LocationDesc'.

        Parameters:
            question (str): The question for which to calculate the mean.

        Returns:
            str: The mean values for each location in JSON format.
        """
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=True).to_json()
        
    def state_mean(self, question: str, state: str):
        """
        Calculate the mean value of a specific question for a given state.

        Parameters:
        - question (str): The question for which the mean value is calculated.
        - state (str): The state for which the mean value is calculated.

        Returns:
        - str: A JSON string containing the mean value of the question for the state.
        """
        return lambda : json.dumps({
            state : self.df.loc[(self.df['Question'] == question) & (self.df['LocationDesc'] == state)]['Data_Value'].mean()
        })
    
    def best5(self, question: str):
        """
        Returns the top 5 locations with the highest or lowest average data value for a given question.

        Parameters:
            question (str): The question for which the average data value is calculated.

        Returns:
            str: A JSON string containing the top 5 locations and their average data values.
        """
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=(question in self.questions_best_is_min)).head(5).to_json()
    
    def worst5(self, question: str):
        """
        Returns the worst 5 locations based on the average data value for a given question.

        Args:
            question (str): The question for which to calculate the worst 5 locations.

        Returns:
            str: A JSON string containing the worst 5 locations and their average data values.
        """
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=(question in self.questions_best_is_max)).head(5).to_json()
    
    def global_mean(self, question: str):
        """
        Calculate the global mean of the specified question.

        Parameters:
        - question (str): The question for which to calculate the global mean.

        Returns:
        - str: A JSON string containing the global mean value.

        Example Usage:
        ```
        data_ingestor = DataIngestor()
        result = data_ingestor.global_mean("Question 1")
        print(result)
        ```
        """
        return lambda: json.dumps({
            "global_mean": self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
        })
    
    def diff_from_mean(self, question: str):
        """
        Calculates the difference from the mean for a given question.

        Parameters:
        - question (str): The question for which to calculate the difference.

        Returns:
        - function: A function that calculates the difference from the mean for the given question.
        """

        def aux():
            gm = self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
            return self.df.loc[self.df['Question'] == question] \
                .groupby('LocationDesc')['Data_Value'].apply(lambda x: gm - x.mean()).to_json()

        return aux
    
    def state_diff_from_mean(self, question: str, state: str):
        """
        Calculates the difference between the mean value of a question and the mean value of that question in a specific state.

        Args:
            question (str): The question for which the difference is calculated.
            state (str): The state for which the difference is calculated.

        Returns:
            function: A function that calculates the difference between the mean values.

        Example:
            diff_func = state_diff_from_mean("Question 1", "California")
            diff = diff_func()
            print(diff)  # Output: {"California": -0.5}
        """
        def aux():
            gm = self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
            return json.dumps({
                state : gm - self.df.loc[(self.df['Question'] == question) & (self.df['LocationDesc'] == state)]['Data_Value'].mean()
            })
        return aux
    
    def mean_by_category(self, question: str):
        """
        Calculate the mean of the 'Data_Value' column by category.

        Parameters:
        - question (str): The question for which the mean is calculated.

        Returns:
        - function: A function that calculates the mean by category when called.

        Example usage:
        ```
        mean_func = mean_by_category('Question1')
        result = mean_func()
        print(result)
        ```

        Note: The returned function should be called to get the mean by category.
        """
        def aux():
            return self.df.loc[self.df['Question'] == question] \
                .groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean().to_json()
        return aux
    
    def state_mean_by_category(self, question: str, state: str):
        """
        Returns a JSON string containing the mean values of 'Data_Value' grouped by 'StratificationCategory1' and 'Stratification1'
        for a given 'question' and 'state'.

        Parameters:
            question (str): The question for which the mean values are calculated.
            state (str): The state for which the mean values are calculated.

        Returns:
            str: A JSON string containing the mean values grouped by 'StratificationCategory1' and 'Stratification1'.
        """
        def aux():
            return json.dumps({
                state : json.loads(self.df.loc[(self.df['Question'] == question) & (self.df['LocationDesc'] == state)] \
                .groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean().to_json())
                })
        return aux
