import os
import sys
import requests
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    raw_data_path: str=os.path.join('artifacts',"data_main1.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def fetch_and_process_data(self, food_type):
        url = "https://edamam-recipe-search.p.rapidapi.com/search"
        querystring = {"q": food_type}
        headers = {
            "X-RapidAPI-Key": "Get this api in RapidApi.com.. diet food api../ not authorized to published",
            "X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        api_data  = response.json()
        
        processed_data = self.preprocess_json(api_data)
        data_dataframe = pd.DataFrame(processed_data)
        
        nutrition_data = self.create_food_nutrition(api_data)
        nutrition_data_dataframe = pd.DataFrame(nutrition_data)
        nutrition_df = nutrition_data_dataframe.pivot_table(index='food_name', columns='label', values='daily')

        # Reset the index to make 'food_name' a regular column
        nutrition_df.reset_index(inplace=True)
        nutrition_df = nutrition_df.drop(nutrition_df.columns[5:26], axis=1)
        
        df = pd.merge(data_dataframe, nutrition_df, on='food_name', how='outer')

        return df

    def preprocess_json(self, data_json):
        reciepe = []
        for item in data_json['hits']:
            data = {
                'food_name' : item['recipe']['label'],
                'food_image' : item['recipe']['image'],
                'food_dietLabels' : item['recipe']['dietLabels'],
                'food_healthLabels' : item['recipe']['healthLabels'],
                'food_calories' : item['recipe']['calories'],
                'food_mealType' : item['recipe']['mealType'],
                'food_digest' : item['recipe']['digest']
            }
            reciepe.append(data)
        return reciepe    

    def create_food_nutrition(self, data_json):
        nutrition = []
        for item in data_json['hits']:
            for i in item['recipe']['digest']:
                d = {
                    'food_name' : item['recipe']['label'],
                    'label': i['label'],
                    'daily': i['daily']
                }
                nutrition.append(d)
        return nutrition

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            food_types = ["chicken", "beef", 'vegetable', "egg", "keto", "fish", "fruit", "breakfast", "tea", "coffee"]

            dataframes = []  # Empty list to store all DataFrames
            for i in food_types:
                df = self.fetch_and_process_data(i)
                dataframes.append(df)  # Append each DataFrame to the list

            # Concatenate all DataFrames together
            all_data = pd.concat(dataframes, ignore_index=True)

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            all_data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Data ingestion is completed")
            return all_data

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj = DataIngestion()
    data = obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    preprocessed_data = data_transformation.data_preprocessing(data)
    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(preprocessed_data))


# from data_transformation import DataTransformation

# # Let's say `food_dataset` is your DataFrame
# food_dataset = ...

# # Create an object of DataTransformation class
# dt = DataTransformation()

# # Perform preprocessing
# preprocessed_data = dt.data_preprocessing(food_dataset)
