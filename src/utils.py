import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)

# your pre-processing functions
def calculate_BMI(weight,height):
    try:
        height_in_M = height/100
        return weight/height_in_M**2
    except Exception as e:
        raise CustomException(e, sys)


def calculate_BMR(weight,height,age,gender):

    try:
        BMI = 1
        if gender == 0 :
            BMI = 447.593 + (9.247*weight) + (3.098*height) - (4.330*age)
            return BMI
        elif gender == 1 :
            BMI = 88.362 + (13.397*weight) + (4.799*height) - (5.677*age)
            return BMI
    except Exception as e:
        raise CustomException(e, sys)
    
def needed_cal(activity,BMR):
    try:
        if activity == 0 :
            return BMR*1.2
        elif activity == 1:
            return BMR*1.375
        elif activity ==2:
            return BMR * 1.55
        elif activity == 3:
            return BMR * 1.725
        else:
            return BMR * 1.9
        
    except Exception as e:
        raise CustomException(e, sys)
    
def calculate_calory_u(input):
    try:
        
        BMI = calculate_BMI(int(input['weight']),int(input['height']))

        BMR = calculate_BMR(int(input['weight']),int(input['height']),int(input['age']),int(input['sex']))

        daily_calory_needed = needed_cal(int(input['activity_lavel']), BMR)

        print("Your body mass index is: ", BMI)
        if ( BMI < 16):
            print("Acoording to your BMI, you are Severely Underweight")
            return {'daily_calory' : [daily_calory_needed+500, 100,406,10,96,11], 
                    'message':"Acoording to your Data, you are Severely Underweight", "BMI":BMI, 'cal': daily_calory_needed+500}
        elif ( BMI >= 16 and BMI < 18.5):
            print("Acoording to your BMI, you are Underweight")
            return {'daily_calory' : [daily_calory_needed+300, 100,406,10,96,11], 
                    'message':"Acoording to your Data, you are Underweight", "BMI":BMI, 'cal': daily_calory_needed+300}
        elif ( BMI >= 18.5 and BMI < 25):

            print("Acoording to your BMI, you are Healthy")

            return {'daily_calory' : [daily_calory_needed, 100,406,10,96,11], 
                    'message':"Acoording to your Data, you are Healthy", "BMI":BMI, 'cal': daily_calory_needed}
        elif ( BMI >= 25 and BMI < 30):

            print("Acoording to your BMI, you are Overweight")
            return {'daily_calory' : [daily_calory_needed-300, 100,406,10,96,11], 
                    'message':"Acoording to your Data, you are Overweight", "BMI":BMI, 'cal': daily_calory_needed-300}
        elif ( BMI >=30):
            print("Acoording to your BMI, you are Severely Overweight")
            return {'daily_calory' : [daily_calory_needed-500, 100,406,10,96,11], 
                    'message':"Acoording to your Data, you are Severely Overweight", "BMI":BMI, 'cal': daily_calory_needed-500}
        
    except Exception as e:
        raise CustomException(e, sys)
    