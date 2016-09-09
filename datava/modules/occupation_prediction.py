# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:30:31 2016

@author: shebashir
"""

import requests
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


class PredictiveModels:
    """ creates a classification model using data from the ONET to predict a job based on an
    individuals personal ranking of ~30 of their own skills.
    """

    def __init__(self):
        # get data on jobs and relevant skills
        #todo: load data on github
        skill_df = pd.read_csv(r'/home/ubuntu/vadatathon/DataVA-datathon/datava/static/skills_df.txt')
        self.job_names_map = skill_df[['O*NET-SOC Code','detailed']]

        self.model = self.build_model(skill_df)
        self.y = skill_df.detailed   # response

    def predict(self, prediction):
        """ predict which college majors match a users skillset

        :param prediction: a list of users self-rated scores for all required skills

        :return: a dataframe of cips, college majors, and probabilities sorted acsending by  top probability matches
        """
        pred = self.model.predict_proba(prediction)
        df = zip(self.y, pred[0])
        df = pd.DataFrame(df, columns=['detailed', 'prob'])
        df.sort_values('prob', ascending=False, inplace=True)
        df = df[0:10]

        merge_df = pd.merge(df, self.job_names_map, on='detailed', how='left')

        # filter to only jobs that end with .00 in ONET
        new_df = []
        for ind, row in merge_df.iterrows():
            if row['O*NET-SOC Code'][-2:] == '00':
                new_df.append([row['O*NET-SOC Code'][0:-3].replace('-',''),
                               row['detailed'],
                               row['prob']])

        df = pd.DataFrame(new_df, columns=['soc', 'job', 'prob'])

        return df

#        career_ids = self.cip_names_and_ids['id']
#        career_names = self.cip_names_and_ids['name_long']
#        df = zip(career_ids, pred[0], career_names)
#        df = pd.DataFrame(df, columns=['cip', 'prob', 'name_long'])

#        df.sort_values('prob', ascending=False, inplace=True)

#        return df[0:10]

    def build_model(self, skill_df):
        X = skill_df[skill_df.columns[1:-4]] # feature matrix
        y = skill_df.detailed   # response
        self.y = y

        knn = KNeighborsClassifier(n_neighbors=10, weights='distance')
        knn.fit(X, y)

        return knn

if __name__ == "__main__":
    p = PredictiveModels()
    g = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    pred = p.predict(g)
    print pred


