
import os
import sys
from dataclasses import dataclass
from sklearn.neighbors import NearestNeighbors
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, calculate_BMI, calculate_BMR, needed_cal, calculate_calory_u
import pandas as pd


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, data):
        try:
            logging.info("Initiating the training of the NearestNeighbors model")

            # Select columns
            a = pd.concat([data.iloc[:, 4], data.iloc[:, 6:11]], axis=1)
            X_train = a.values

            # Initialize NearestNeighbors class
            nn_model = NearestNeighbors(n_neighbors=4)

            # Fit the model to your data
            nn_model.fit(X_train)

            logging.info(f"NearestNeighbors model training completed")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = nn_model
            )
            return 'train_complete'

        except Exception as e:
            raise CustomException(e, sys)