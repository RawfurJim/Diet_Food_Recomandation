import sys
import pandas as pd
import numpy as np
import os
from src.utils import load_object, save_object, calculate_BMI, calculate_BMR, needed_cal, calculate_calory_u
from src.exception import CustomException

class PredictPipeline:
    def __init__(self):
        self.preprocessor_path = os.path.join('artifacts','preprocessor.pkl')
        self.model_path = os.path.join("artifacts","model.pkl")

    def get_nearest_neighbors(self, data, point, n_neighbors=4):
        # Load model
        model = load_object(file_path=self.model_path)

        # Find the nearest neighbors to your point
        distances, indices = model.kneighbors(point)

        return indices, distances

    def recomanded_food(self, user_input):
        try:
            data = load_object(file_path=self.preprocessor_path)
            breakfast_data = data[data['breakfast'] == 1]
            lunch_data = data[data['lunch'] == 1]
            dinner_data = data[data[' dinner'] == 1]
            user_value = user_input['daily_calory']
            point = np.array(user_value).reshape(1, -1)

            # Calculate proportion for each meal
            breakfast_proportion = 0.3
            lunch_proportion = 0.4
            dinner_proportion = 0.3

            # Define points for each meal type
            breakfast_point = (point * breakfast_proportion).reshape(1, -1)
            lunch_point = (point * lunch_proportion).reshape(1, -1)
            dinner_point = (point * dinner_proportion).reshape(1, -1)

            # Find nearest neighbors for each meal type
            breakfast_indices, breakfast_distances = self.get_nearest_neighbors(breakfast_data, breakfast_point)
            lunch_indices, lunch_distances = self.get_nearest_neighbors(lunch_data, lunch_point)
            dinner_indices, dinner_distances = self.get_nearest_neighbors(dinner_data, dinner_point)

            all_indices = breakfast_indices[0] + lunch_indices[0] + dinner_indices[0]

            merged_list = []
            merged_list.extend(breakfast_indices[0])
            merged_list.extend(lunch_indices[0])
            merged_list.extend(dinner_indices[0])

            food = []
            for i in merged_list:
                list = [data.loc[i, 'food_name'], data.loc[i, 'image'], data.loc[i, 'food_calories'], data.loc[i,'food_healthLabels']]
                food.append(list)

            result = {'recomanded_food': food, 'message': user_input['message'], 'BMI': user_input['BMI'], 'cal': user_input['cal']}
            return result
        except Exception as e:
            raise CustomException(e, sys)
