import pickle
import pandas as pd

with open(r'C:\Users\HP\Desktop\Diet_Food_Recomandetion\artifacts\preprocessor.pkl', 'rb') as f:
    data = pickle.load(f)

df = pd.DataFrame(data)

print(df.info())