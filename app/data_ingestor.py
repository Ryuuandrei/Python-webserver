import os
import json
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
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
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=True).to_json()
        
    def state_mean(self, question: str, state: str):
        return lambda : json.dumps({
            state : self.df.loc[(self.df['Question'] == question) & (self.df['LocationDesc'] == state)]['Data_Value'].mean()
            })
    
    def best5(self, question: str):
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=(question in self.questions_best_is_min)).head(5).to_json()
    
    def worst5(self, question: str):
        return lambda : self.df.loc[self.df['Question'] == question] \
            .groupby('LocationDesc')['Data_Value'].mean().sort_values(ascending=(question in self.questions_best_is_max)).head(5).to_json()
    
    def global_mean(self, question: str):
        return lambda : json.dumps({
            "global_mean": self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
            })
    
    def diff_from_mean(self, question: str):
        def aux():
            gm = self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
            return self.df.loc[self.df['Question'] == question] \
                .groupby('LocationDesc')['Data_Value'].apply(lambda x: gm - x.mean()).to_json()
        return aux
    
    def state_diff_from_mean(self, question: str, state: str):
        def aux():
            gm = self.df.loc[self.df['Question'] == question]['Data_Value'].mean()
            return json.dumps({
                state : gm - self.df.loc[(self.df['Question'] == question) & (self.df['LocationDesc'] == state)]['Data_Value'].mean()
            })
        return aux
    
    def mean_by_category(self, question: str):
        def aux():
            return self.df.loc[self.df['Question'] == question] \
                .groupby(['LocationDesc', 'StratificationCategory1'])['Stratification1'].mean().to_json()
        return aux
