# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:30:31 2016

@author: shebashir
"""

import requests
import pandas as pd


class DataUsaNamesAndIds:
    """ creates a classification model using data from the DataUSA api to predict a college major based on an
    individuals personal ranking of ~30 of their own skills.

    Notes: There are ~1700 college majors with a single instance of each.
    """

    def __init__(self):
        self.skill_names_and_ids = self.get_skill_names_and_ids()

    @staticmethod
    def get_skill_names_and_ids():
        """ request the full listing of skill ids and full text names from the DataUSA api

        :return: full listing of cip (college major) ids and full text names
        """

        r = requests.get(r'http://api.datausa.io/attrs/skill/')  # get id to name matches
        skill_data = r.json()

        headers = skill_data['headers']
        data = skill_data['data']

        skill_id_df = pd.DataFrame(data, columns=headers)
        skill_names_and_ids = skill_id_df[['id','name','parent']]
        skill_names_and_ids = skill_names_and_ids.sort_values(by='id')
        skill_names_and_ids.reset_index(inplace=True)

        return skill_names_and_ids
