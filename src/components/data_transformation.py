import sys
import pandas as pd
import os
from src.utils import save_object
from src.exception import CustomException
from dataclasses import dataclass



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def data_preprocessing(self, data):
        """
        Data preprocessing function
        """
        try:
            # Your preprocessing steps
            data = data.drop(columns='food_digest')
            
            new_mealtype = []
            for i in data['food_mealType']:
            
                
            
                if i == "['brunch']":
                
                    new_mealtype.append(['breakfast', 'lunch/dinner'])
                
                    
                    
                elif i == "['teatime']":
                    new_mealtype.append(['breakfast'])
                
                    
                elif i == "['snack']":
                    new_mealtype.append(['breakfast'])
                
                    
                elif i == "['teatime', 'lunch/dinner']":
                    new_mealtype.append(['breakfast', 'lunch/dinner'])
                
                    
                else:
                    new_mealtype.append(eval(str(i)))


            data['mealType'] = new_mealtype
            
            new_list = [', '.join(s[0].split('/')) for s in data['mealType']]
            data['check_type'] = new_list
            meal_df1 = data['check_type'].str.get_dummies(',')
            data = pd.concat([data, meal_df1], axis=1)
            
            # Your conditional operation
            a = [i % 10 + 1 for i in range(100)]
            food_list = []
            for j, i in enumerate(a) :
    
                if j>=0 and j<=9:
                    food_list.append(f'static\\images\\chicken_{i}.jpg')
                elif j>9 and j<=19:
                    food_list.append(f'static\\images\\meat_{i}.jpg')
                elif j>19 and j<=29:
                    food_list.append(f'static\\images\\vege_{i}.jpg')
                elif j>29 and j<=39:
                    food_list.append(f'static\\images\\egg_{i}.jpg')
                elif j>39 and j<=49:
                    food_list.append(f'static\\images\\keto_{i}.jpg')
                elif j>49 and j<=59:
                    food_list.append(f'static\\images\\fish_{i}.jpg')
                elif j>59 and j<=69:
                    food_list.append(f'static\\images\\fruit_{i}.jpg')
                elif j>69 and j<=79:
                    food_list.append(f'static\\images\\break_{i}.jpg')
                elif j>79 and j<=89:
                    food_list.append(f'static\\images\\tea_{i}.jpg')
                elif j>89 and j<=99:
                    food_list.append(f'static\\images\\coffee_{i}.jpg')
            data['image'] = food_list
            # Drop unnecessary meal types
            data.drop(columns=['snack', 'teatime', 'brunch'], inplace=True, errors='ignore')
            # Save preprocessed data as pickle
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path, obj=data)

            return data

        except Exception as e:
            raise CustomException(e,sys)
        

# from data_transformation import DataTransformation

# # Let's say `data` is your DataFrame
# food_dataset = ...

# # Create an object of DataTransformation class
# dt = DataTransformation()

# # Perform preprocessing
# preprocessed_data = dt.data_preprocessing(food_dataset)