from flask import Flask, render_template, request
import pickle
from src.pipeline.predict_pipeline import PredictPipeline
from src.utils import calculate_calory_u


poplar_df = pickle.load(open('artifacts/preprocessor.pkl','rb'))

app = Flask(__name__)

pipeline = PredictPipeline()

@app.route('/')
def index():
    return render_template('index.html',
                           food_name = list(poplar_df['food_name'].values),
                           food_image = list(poplar_df['image'].values),
                           food_healthlabel = list(poplar_df['food_healthLabels'].values))

@app.route('/recommended')
def recomand_ui():
    return render_template('recommended.html')

@app.route('/recommended_foods', methods=['POST'])
def recomand():
    age = request.form.get('age')
    weight = request.form.get('weight')
    height = request.form.get('height')
    gender = request.form.get('gender')
    active = request.form.get('activity_lavel')

    input = {
        'weight': str(weight),
        'height': str(height),
        'age': str(age),
        'sex': str(gender),
        'activity_lavel': str(active)
    }

    user_input = calculate_calory_u(input)
    recommended_food = pipeline.recomanded_food(user_input)

    return render_template('recommended.html', data = recommended_food ) 

if __name__ == '__main__':
    app.run(debug=True)